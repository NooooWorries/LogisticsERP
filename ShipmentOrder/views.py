from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from ShipmentOrder.forms import OrderCreationOneForm, OrderCreationTwoForm, OrderCreationThreeForm, OrderModityForm
from ShipmentOrder.models import ShipmentOrder, Goods
from Customers.models import Customer
from django.core import serializers
from django.db.models import Q
import json
import datetime
import barcode
from django.template.loader import get_template
from xhtml2pdf import pisa
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from LogisticsERP import settings, utils
import os
from xhtml2pdf.default import DEFAULT_FONT
from barcode.writer import ImageWriter
from ShipmentOrder.utils import calculate_freight, calculate_density, rearrange_pack_number
from django.contrib.staticfiles.templatetags.staticfiles import static


# 添加订单 第一步 基本信息
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def add_order_stage_one(request):
    request.session.set_expiry(request.session.get_expiry_age())
    role = utils.get_user_type(request)
    if role != 0 and role != 1 and role != 2:
        return render(request, 'error/permission.html')
    if request.method == 'POST':
        form = OrderCreationOneForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.create_date = datetime.datetime.now().strftime("%Y-%m-%d")
            order.handle = request.user
            order.save()
            request.session['order'] = order.id
            return add_order_stage_two(request, order)
    else:
        form = OrderCreationOneForm()
    return render(request, "order/add/form-addorder-1.html", {'form': form})


# 添加订单 第一步 选择客户
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def add_order_select_customer(request, customer_id):
    request.session.set_expiry(request.session.get_expiry_age())
    role = utils.get_user_type(request)
    if role != 0 and role != 1 and role != 2:
        return render(request, 'error/permission.html')
    customer_instance = Customer.objects.filter(pk=customer_id)
    data = serializers.serialize('json', customer_instance)
    return HttpResponse(json.dumps(data), content_type="application/json")


# 添加订单 第二步 货物信息显示
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def add_order_stage_two(request, order):
    request.session.set_expiry(request.session.get_expiry_age())
    role = utils.get_user_type(request)
    if role != 0 and role != 1 and role != 2:
        return render(request, 'error/permission.html')
    if "order" not in request.session:
        return render(request, 'error/redirect_error.html')
    form = OrderCreationTwoForm()
    return render(request, "order/add/form-addorder-2.html", {'form': form, 'order': order})


# 添加订单 第二步 货物信息添加 ajax
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def ajax_add_goods(request):
    request.session.set_expiry(request.session.get_expiry_age())
    role = utils.get_user_type(request)
    if role != 0 and role != 1 and role != 2:
        return render(request, 'error/permission.html')
    if "order" not in request.session:
        return render(request, 'error/redirect_error.html')
    form = OrderCreationTwoForm(request.POST)
    order = request.session['order']
    if form.is_valid():
        pack_count = Goods.objects.filter(shipment_order_id_id=order).count()
        new_good = Goods(
            shipment_order_id_id=order,
            pack_number=pack_count + 1,
            goods_name=request.POST.get('goods_name'),
            amount=request.POST.get('amount'),
            weight=request.POST.get('weight'),
            unit_price=request.POST.get('unit_price'),
        )
        new_good.freight = float(new_good.weight) * float(new_good.unit_price)
        new_good.save()
        good = Goods.objects.filter(shipment_order_id_id=order)
        rearrange_pack_number(good)
        data = serializers.serialize('json', good)
        # 更新运费
        order_instance = get_object_or_404(ShipmentOrder, pk=order)
        calculate_freight(order_instance, good)
        order_instance.save()

        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        print(form.errors)


# 添加订单 第二步 货物信息删除
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def ajax_delete_goods(request, good_id):
    request.session.set_expiry(request.session.get_expiry_age())
    role = utils.get_user_type(request)
    if role != 0 and role != 1 and role != 2:
        return render(request, 'error/permission.html')
    if "order" not in request.session:
        return render(request, 'error/redirect_error.html')
    order = request.session['order']
    goods_object = Goods.objects.get(id=good_id)
    goods_object.delete()
    good = Goods.objects.filter(shipment_order_id_id=order)
    rearrange_pack_number(good)
    data = serializers.serialize('json', good)

    # 更新运费
    order_instance = get_object_or_404(ShipmentOrder, pk=order)
    calculate_freight(order_instance, good)
    order_instance.save()

    return HttpResponse(json.dumps(data), content_type="application/json")


# 添加订单 第三步骤 页面跳转
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def add_order_stage_three_redirect(request):
    request.session.set_expiry(request.session.get_expiry_age())
    role = utils.get_user_type(request)
    if role != 0 and role != 1 and role != 2:
        return render(request, 'error/permission.html')
    if "order" not in request.session:
        return render(request, 'error/redirect_error.html')
    order = request.session['order']
    order_instance = ShipmentOrder.objects.get(pk=order)

    if request.method == 'POST':
        form = OrderCreationThreeForm(request.POST)
        if form.is_valid():
            order_instance.packingFee = float(request.POST.get("packingFee"))
            order_instance.insurance_fee = float(request.POST.get("claimed_value")) * float(request.POST.get("insurance_rate")) / 100
            order_instance.totalPrice = float(order_instance.freight) + float(order_instance.insurance_fee) - \
                                        order_instance.paymentOnAccountFreight + order_instance.packingFee
            order_instance.payable = order_instance.totalPrice
            order_instance.volume = form.cleaned_data["volume"]
            order_instance.claimed_value = form.cleaned_data["claimed_value"]
            order_instance.insurance_rate = form.cleaned_data["insurance_rate"]

            # 计算密度
            good_instance = Goods.objects.filter(shipment_order_id_id=order)
            calculate_density(order_instance, good_instance)
            order_instance.save()
            return add_order_summary(request)
    else:
        form = OrderCreationThreeForm()
        return render(request, "order/add/form-addorder-3.html", {'form': form, 'order': order_instance})


# 添加订单 第四步 信息确认
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def add_order_summary(request):
    request.session.set_expiry(request.session.get_expiry_age())
    role = utils.get_user_type(request)
    if role != 0 and role != 1 and role != 2:
        return render(request, 'error/permission.html')
    if "order" not in request.session:
        return render(request, 'error/redirect_error.html')
    order = request.session['order']
    order_instance = ShipmentOrder.objects.get(pk=order)
    goods_instance = Goods.objects.filter(shipment_order_id_id=order)
    return render(request, "order/add/form-addorder-summary.html", {'order': order_instance, 'good': goods_instance})


# 添加订单 第五步 交由审核
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def add_order_audit(request):
    request.session.set_expiry(request.session.get_expiry_age())
    role = utils.get_user_type(request)
    if role != 0 and role != 1 and role != 2:
        return render(request, 'error/permission.html')
    if "order" not in request.session:
        form_create = OrderCreationOneForm()
        return render(request, "order/add/form-addorder-1.html", {'form': form_create})
    order = request.session['order']
    order_instance = ShipmentOrder.objects.get(pk=order)
    goods_instance = Goods.objects.filter(shipment_order_id_id=order)
    if goods_instance.count() >= 1:
        order_instance.status = 1
        order_instance.save()
        message = "您的订单已经交由审核"
    else:
        message = "无法提交审核，原因：没有货物。请前往草稿箱修改订单"
    return render(request, "order/add/form-addorder-submitted.html", {'message': message})


# 查询订单 管理端 所有订单
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def track_order_manager(request):
    request.session.set_expiry(request.session.get_expiry_age())
    try:
        curPage = int(request.GET.get('curPage', '1'))
        allPage = int(request.GET.get('allPage', '1'))
        pageType = str(request.GET.get('pageType', ''))
    except ValueError:
        curPage = 1
        allPage = 1
        pageType = ''
    # 判断点击了【下一页】还是【上一页】
    if pageType == 'pageDown':
        curPage += 1
    elif pageType == 'pageUp':
        curPage -= 1
    startPos = (curPage - 1) * settings.ONE_PAGE_OF_DATA
    endPos = startPos + settings.ONE_PAGE_OF_DATA
    order_list = ShipmentOrder.objects.all()[startPos:endPos]
    if curPage == 1 and allPage == 1:  # 标记1
        allPostCounts = ShipmentOrder.objects.count()
        allPage = int(allPostCounts / settings.ONE_PAGE_OF_DATA)
        remainPost = allPostCounts % settings.ONE_PAGE_OF_DATA
        if remainPost > 0:
            allPage += 1
    return render(request, "order/manage/trackorder-manager.html", {'order': order_list,
                                                                    'allPage': allPage,
                                                                    'curPage': curPage
                                                                    })


# 查询订单 详情页
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def track_order_detail(request, order_id):
    request.session.set_expiry(request.session.get_expiry_age())
    order = get_object_or_404(ShipmentOrder, pk=order_id)
    good = Goods.objects.filter(shipment_order_id_id=order_id)
    return render(request, "order/manage/trackorder-detail.html", {'order': order, 'good': good})


# 查询订单 编辑页
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def track_order_modify(request, order_id):
    request.session.set_expiry(request.session.get_expiry_age())
    role = utils.get_user_type(request)
    if role != 0 and role != 1 and role != 2:
        return render(request, 'error/permission.html')
    request.session['order_manage'] = order_id
    goods_instance = Goods.objects.filter(shipment_order_id_id=order_id)
    goods_form = OrderCreationTwoForm(request.POST or None)

    return render(request, "order/manage/trackorder-modify.html", {'good_form': goods_form,
                                                                   'good_instance': goods_instance,
                                                                   'order': order_id})


# 查询订单 编辑页 2
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def track_order_modify_2(request, order_id):
    request.session.set_expiry(request.session.get_expiry_age())
    role = utils.get_user_type(request)
    if role != 0 and role != 1 and role != 2:
        return render(request, 'error/permission.html')
    order_instance = get_object_or_404(ShipmentOrder, id=order_id)
    order_form = OrderModityForm(request.POST or None, instance=order_instance)
    goods_instance = Goods.objects.filter(shipment_order_id_id=order_id)
    if request.method == 'POST':
        if order_form.is_valid():
            sum_freight = 0
            for item in goods_instance:
                sum_freight += item.freight
            order_instance.freight = sum_freight
            order_instance.insurance_fee = float(request.POST.get("claimed_value")) * float(
                request.POST.get("insurance_rate")) / 100
            order_instance.totalPrice = float(order_instance.freight) + float(order_instance.insurance_fee) - \
                                        order_instance.paymentOnAccountFreight + order_instance.packingFee
            # 计算密度
            good_instance = Goods.objects.filter(shipment_order_id_id=order_id)
            calculate_density(order_instance, good_instance)
            order_form.save(freight=order_instance.freight, insurance=order_instance.insurance_fee)
            return render(request, 'order/manage/trackorder-modify-complete.html')
    return render(request, "order/manage/trackorder-modify-2.html", {'form': order_form,
                                                                   'good_instance': goods_instance,
                                                                   'order': order_id})


# 修改订单 货物信息删除 ajax
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def ajax_delete_goods_manage(request, good_id):
    request.session.set_expiry(request.session.get_expiry_age())
    role = utils.get_user_type(request)
    if role != 0 and role != 1 and role != 2:
        return render(request, 'error/permission.html')
    goods_object = Goods.objects.get(id=good_id)
    goods_object.delete()
    good = Goods.objects.filter(shipment_order_id_id=request.session['order_manage'])
    rearrange_pack_number(good)
    data = serializers.serialize('json', good)
    # 计算运费
    order_instance = get_object_or_404(ShipmentOrder, pk=request.session['order_manage'])
    calculate_freight(order_instance, good)
    # 计算密度
    calculate_density(order_instance, good)
    order_instance.save()
    return HttpResponse(json.dumps(data), content_type="application/json")


# 修改订单 货物信息添加 ajax
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def ajax_add_goods_manage(request):
    request.session.set_expiry(request.session.get_expiry_age())
    role = utils.get_user_type(request)
    if role != 0 and role != 1 and role != 2:
        return render(request, 'error/permission.html')
    goods_form = OrderCreationTwoForm(request.POST)
    order = request.session['order_manage']
    if goods_form.is_valid():
        pack_count = Goods.objects.filter(shipment_order_id_id=order).count()
        new_good = Goods(
            shipment_order_id_id=order,
            pack_number=pack_count + 1,
            goods_name=request.POST.get('goods_name'),
            amount=request.POST.get('amount'),
            weight=request.POST.get('weight'),
            unit_price=request.POST.get('unit_price'),
        )
        new_good.freight = float(new_good.weight) * float(new_good.unit_price)
        new_good.save()
        good = Goods.objects.filter(shipment_order_id_id=order)
        rearrange_pack_number(good)
        data = serializers.serialize('json', good)
        # 计算密度
        order_instance = get_object_or_404(ShipmentOrder, pk=order)
        calculate_density(order_instance, good)
        order_instance.save()
        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        print(goods_form.errors)


# 管理订单 确认删除
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def track_order_confirm_delete(request, order_id):
    request.session.set_expiry(request.session.get_expiry_age())
    role = utils.get_user_type(request)
    if role != 0 and role != 1 and role != 2:
        return render(request, 'error/permission.html')
    order_instance = ShipmentOrder.objects.get(pk=order_id)
    goods_instance = Goods.objects.filter(shipment_order_id_id=order_id)
    return render(request, "order/manage/trackorder-delete-confirm.html", {'order': order_instance, 'good': goods_instance})


# 管理订单 订单删除
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def track_order_delete(request, order_id):
    request.session.set_expiry(request.session.get_expiry_age())
    role = utils.get_user_type(request)
    if role != 0 and role != 1 and role != 2:
        return render(request, 'error/permission.html')
    order_object = get_object_or_404(ShipmentOrder, pk=order_id)
    if order_object.handle == request.user and order_object.status == 0:
        request.session['draft'] = request.session['draft'] - 1
    order_object.delete()
    return render(request, "order/manage/trackorder-delete-complete.html")


# 管理订单 订单搜索
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def track_order_search(request):
    request.session.set_expiry(request.session.get_expiry_age())
    query = request.GET.get('query')
    try:
        curPage = int(request.GET.get('curPage', '1'))
        allPage = int(request.GET.get('allPage', '1'))
        pageType = str(request.GET.get('pageType', ''))
    except ValueError:
        curPage = 1
        allPage = 1
        pageType = ''
        # 判断点击了【下一页】还是【上一页】
    if pageType == 'pageDown':
        curPage += 1
    elif pageType == 'pageUp':
        curPage -= 1
    startPos = (curPage - 1) * settings.ONE_PAGE_OF_DATA
    endPos = startPos + settings.ONE_PAGE_OF_DATA
    all_order = ShipmentOrder.objects.filter(
        Q(sender__icontains=query)|
        Q(from_address__icontains=query)|
        Q(sender_contact__icontains=query)|
        Q(receiver__icontains=query)|
        Q(to_address__icontains=query)|
        Q(receiver_contact__icontains=query)|
        Q(mode__icontains=query)|
        Q(comments__icontains=query)).count()
    order = ShipmentOrder.objects.filter(
        Q(sender__icontains=query)|
        Q(from_address__icontains=query)|
        Q(sender_contact__icontains=query)|
        Q(receiver__icontains=query)|
        Q(to_address__icontains=query)|
        Q(receiver_contact__icontains=query)|
        Q(mode__icontains=query)|
        Q(comments__icontains=query))[startPos:endPos]
    if curPage == 1 and allPage == 1:  # 标记1
        allPostCounts = all_order
        allPage = int(allPostCounts / settings.ONE_PAGE_OF_DATA)
        remainPost = allPostCounts % settings.ONE_PAGE_OF_DATA
        if remainPost > 0:
            allPage += 1
    return render(request, "order/manage/trackorder-manager.html", {'order': order,
                                                                    'query': query,
                                                                    'allPage': allPage,
                                                                    'curPage': curPage})


# 管理订单 订单高级搜索
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def track_order_search_advanced(request):
    request.session.set_expiry(request.session.get_expiry_age())
    return render(request, "order/search/trackorder-search.html")


# 管理订单 订单高级搜索结果
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def track_order_search_advanced_result(request):
    request.session.set_expiry(request.session.get_expiry_age())
    keyword = request.GET.get('keyword')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    status = request.GET.get('status')
    if start_date is "": start_date = "1970-1-1"
    if end_date is "": end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    if status is not "":
        status = int(request.GET.get('status'))
        result = ShipmentOrder.objects.filter(
             Q(sender__icontains=keyword) |
             Q(from_address__icontains=keyword) |
             Q(sender_contact__icontains=keyword) |
             Q(receiver__icontains=keyword) |
             Q(to_address__icontains=keyword) |
             Q(receiver_contact__icontains=keyword) |
             Q(mode__icontains=keyword) |
             Q(comments__icontains=keyword),
             Q(create_date__range=(start_date, end_date)),
             Q(status__exact=status))
        result_count = result.count()
    else:
        result = ShipmentOrder.objects.filter(
            Q(sender__icontains=keyword) |
            Q(from_address__icontains=keyword) |
            Q(sender_contact__icontains=keyword) |
            Q(receiver__icontains=keyword) |
            Q(to_address__icontains=keyword) |
            Q(receiver_contact__icontains=keyword) |
            Q(mode__icontains=keyword) |
            Q(comments__icontains=keyword),
            Q(create_date__range=(start_date, end_date)))
        result_count = result.count()

    try:
        curPage = int(request.GET.get('curPage', '1'))
        allPage = int(request.GET.get('allPage', '1'))
        pageType = str(request.GET.get('pageType', ''))
    except ValueError:
        curPage = 1
        allPage = 1
        pageType = ''
    # 判断点击了【下一页】还是【上一页】
    if pageType == 'pageDown':
        curPage += 1
    elif pageType == 'pageUp':
        curPage -= 1
    startPos = (curPage - 1) * settings.ONE_PAGE_OF_DATA
    endPos = startPos + settings.ONE_PAGE_OF_DATA
    order = result[startPos:endPos]
    if curPage == 1 and allPage == 1:  # 标记1
        allPostCounts = result_count
        allPage = int(allPostCounts / settings.ONE_PAGE_OF_DATA)
        remainPost = allPostCounts % settings.ONE_PAGE_OF_DATA
        if remainPost > 0:
            allPage += 1
    return render(request, "order/search/trackorder-search-result.html", {'order': order,
                                                                          'keyword': keyword,
                                                                          'start_date': start_date,
                                                                          'end_date': end_date,
                                                                          'status': status,
                                                                          'allPage': allPage,
                                                                          'curPage': curPage})


# 管理订单 草稿箱
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def track_order_draft(request):
    request.session.set_expiry(request.session.get_expiry_age())
    role = utils.get_user_type(request)
    if role != 0 and role != 1 and role != 2:
        return render(request, 'error/permission.html')
    try:
        curPage = int(request.GET.get('curPage', '1'))
        allPage = int(request.GET.get('allPage', '1'))
        pageType = str(request.GET.get('pageType', ''))
    except ValueError:
        curPage = 1
        allPage = 1
        pageType = ''
    # 判断点击了【下一页】还是【上一页】
    if pageType == 'pageDown':
        curPage += 1
    elif pageType == 'pageUp':
        curPage -= 1
    startPos = (curPage - 1) * settings.ONE_PAGE_OF_DATA
    endPos = startPos + settings.ONE_PAGE_OF_DATA
    order_all = ShipmentOrder.objects.filter(handle=request.user, status=0).count()
    order = ShipmentOrder.objects.filter(handle=request.user, status=0)[startPos: endPos]
    if curPage == 1 and allPage == 1:  # 标记1
        allPostCounts = order_all
        allPage = int(allPostCounts / settings.ONE_PAGE_OF_DATA)
        remainPost = allPostCounts % settings.ONE_PAGE_OF_DATA
        if remainPost > 0:
            allPage += 1
    return render(request, "order/draft/trackorder-draft.html", {'order': order,
                                                                 'allPage': allPage,
                                                                 'curPage': curPage})


# 管理订单 草稿箱 订单搜索
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def track_order_draft_search(request):
    request.session.set_expiry(request.session.get_expiry_age())
    query = request.GET.get('query')
    try:
        curPage = int(request.GET.get('curPage', '1'))
        allPage = int(request.GET.get('allPage', '1'))
        pageType = str(request.GET.get('pageType', ''))
    except ValueError:
        curPage = 1
        allPage = 1
        pageType = ''
    # 判断点击了【下一页】还是【上一页】
    if pageType == 'pageDown':
        curPage += 1
    elif pageType == 'pageUp':
        curPage -= 1
    startPos = (curPage - 1) * settings.ONE_PAGE_OF_DATA
    endPos = startPos + settings.ONE_PAGE_OF_DATA
    all_order = ShipmentOrder.objects.filter(
        Q(sender__icontains=query)|
        Q(from_address__icontains=query)|
        Q(sender_contact__icontains=query)|
        Q(receiver__icontains=query)|
        Q(to_address__icontains=query)|
        Q(receiver_contact__icontains=query)|
        Q(mode__icontains=query)|
        Q(comments__icontains=query), Q(status__exact=0), Q(handle__exact=request.user.id)).count()
    order = ShipmentOrder.objects.filter(
        Q(sender__icontains=query)|
        Q(from_address__icontains=query)|
        Q(sender_contact__icontains=query)|
        Q(receiver__icontains=query)|
        Q(to_address__icontains=query)|
        Q(receiver_contact__icontains=query)|
        Q(mode__icontains=query)|
        Q(comments__icontains=query), Q(status__exact=0), Q(handle__exact=request.user.id))
    if curPage == 1 and allPage == 1:  # 标记1
        allPostCounts = all_order
        allPage = int(allPostCounts / settings.ONE_PAGE_OF_DATA)
        remainPost = allPostCounts % settings.ONE_PAGE_OF_DATA
        if remainPost > 0:
            allPage += 1

    return render(request, "order/draft/trackorder-draft.html", {'order': order,
                                                                 'query': query,
                                                                 'allPage': allPage,
                                                                 'curPage': curPage})


# 管理订单 草稿箱 编辑
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def track_order_draft_modify(request, order_id):
    request.session.set_expiry(request.session.get_expiry_age())
    request.session['order_manage'] = order_id
    order_instance = get_object_or_404(ShipmentOrder, id=order_id)
    order_form = OrderModityForm(request.POST or None, instance=order_instance)
    goods_instance = Goods.objects.filter(shipment_order_id_id=order_id)
    goods_form = OrderCreationTwoForm(request.POST or None)

    if order_form.is_valid():
        goods_instance = Goods.objects.filter(shipment_order_id_id=order_id)
        calculate_freight(order_instance, goods_instance)
        order_form.save(freight=order_instance.freight, insurance=order_instance.insurance_fee)
        # 计算密度
        calculate_density(order_instance, goods_instance)
        # 计算总价
        order_instance.insurance_fee = float(request.POST.get("claimed_value")) * float(
            request.POST.get("insurance_rate")) / 100
        order_instance.totalPrice = float(order_instance.freight) + float(order_instance.insurance_fee) - \
                                    order_instance.paymentOnAccountFreight + order_instance.packingFee
        order_instance.payable = order_instance.totalPrice - order_instance.paid_price
        order_instance.save()
        return render(request, "order/draft/trackorder-draft-modify-complete.html")
    return render(request, "order/draft/trackorder-draft-modify.html", {'form': order_form,
                                                                        'good_form': goods_form,
                                                                        'good_instance': goods_instance,
                                                                        'order': order_id})


# 管理订单 提交审核
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def track_order_submit_audit(request, order_id):
    request.session.set_expiry(request.session.get_expiry_age())
    order_instance = ShipmentOrder.objects.get(pk=order_id)
    goods_instance = Goods.objects.filter(shipment_order_id_id=order_id)
    if goods_instance.count() >= 1:
        order_instance.status = 1
        order_instance.save()
        message = "您的订单已经交由审核"
        request.session['draft'] = request.session['draft'] - 1
    else:
        message = "无法提交审核，原因：没有货物。请前往草稿箱修改订单"
    return render(request, "order/draft/trackorder-draft-submitted.html", {'message': message})


# 管理订单 审核订单
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def track_order_audit(request):
    request.session.set_expiry(request.session.get_expiry_age())
    try:
        curPage = int(request.GET.get('curPage', '1'))
        allPage = int(request.GET.get('allPage', '1'))
        pageType = str(request.GET.get('pageType', ''))
    except ValueError:
        curPage = 1
        allPage = 1
        pageType = ''
        # 判断点击了【下一页】还是【上一页】
    if pageType == 'pageDown':
        curPage += 1
    elif pageType == 'pageUp':
        curPage -= 1
    startPos = (curPage - 1) * settings.ONE_PAGE_OF_DATA
    endPos = startPos + settings.ONE_PAGE_OF_DATA
    order_all = ShipmentOrder.objects.filter(status=1).count()
    order = ShipmentOrder.objects.filter(status=1)[startPos:endPos]
    if curPage == 1 and allPage == 1:  # 标记1
        allPostCounts = order_all
        allPage = int(allPostCounts / settings.ONE_PAGE_OF_DATA)
        remainPost = allPostCounts % settings.ONE_PAGE_OF_DATA
        if remainPost > 0:
            allPage += 1
    return render(request, "order/audit/trackorder-audit.html", {'order': order,
                                                                 'allPage': allPage,
                                                                 'curPage': curPage})


# 管理订单 审核订单 订单搜索
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def track_order_audit_search(request):
    request.session.set_expiry(request.session.get_expiry_age())
    query = request.GET.get('query')
    try:
        curPage = int(request.GET.get('curPage', '1'))
        allPage = int(request.GET.get('allPage', '1'))
        pageType = str(request.GET.get('pageType', ''))
    except ValueError:
        curPage = 1
        allPage = 1
        pageType = ''
    # 判断点击了【下一页】还是【上一页】
    if pageType == 'pageDown':
        curPage += 1
    elif pageType == 'pageUp':
        curPage -= 1
    startPos = (curPage - 1) * settings.ONE_PAGE_OF_DATA
    endPos = startPos + settings.ONE_PAGE_OF_DATA
    all_order = ShipmentOrder.objects.filter(
        Q(sender__icontains=query)|
        Q(from_address__icontains=query)|
        Q(sender_contact__icontains=query)|
        Q(receiver__icontains=query)|
        Q(to_address__icontains=query)|
        Q(receiver_contact__icontains=query)|
        Q(mode__icontains=query)|
        Q(comments__icontains=query), Q(status__exact=1)).count()
    order = ShipmentOrder.objects.filter(
        Q(sender__icontains=query)|
        Q(from_address__icontains=query)|
        Q(sender_contact__icontains=query)|
        Q(receiver__icontains=query)|
        Q(to_address__icontains=query)|
        Q(receiver_contact__icontains=query)|
        Q(mode__icontains=query)|
        Q(comments__icontains=query), Q(status__exact=1))[startPos:endPos]
    if curPage == 1 and allPage == 1:  # 标记1
        allPostCounts = all_order
        allPage = int(allPostCounts / settings.ONE_PAGE_OF_DATA)
        remainPost = allPostCounts % settings.ONE_PAGE_OF_DATA
        if remainPost > 0:
            allPage += 1
    return render(request, "order/audit/trackorder-audit.html", {'order': order,
                                                                 'query': query,
                                                                 'allPage': allPage,
                                                                 'curPage': curPage})


# 管理订单 审核订单 编辑
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def track_order_audit_modify(request, order_id):
    request.session.set_expiry(request.session.get_expiry_age())
    request.session['order_manage'] = order_id
    goods_instance = Goods.objects.filter(shipment_order_id_id=order_id)
    goods_form = OrderCreationTwoForm(request.POST or None)
    return render(request, "order/audit/trackorder-audit-modify.html", {'good_form': goods_form,
                                                                        'good_instance': goods_instance,
                                                                        'order': order_id})

# 管理订单 审核订单 编辑 2
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def track_order_audit_modify_2(request, order_id):
    request.session.set_expiry(request.session.get_expiry_age())
    request.session['order_manage'] = order_id
    order_instance = get_object_or_404(ShipmentOrder, id=order_id)
    order_form = OrderModityForm(request.POST or None, instance=order_instance)
    goods_instance = Goods.objects.filter(shipment_order_id_id=order_id)
    if order_form.is_valid():
        calculate_freight(order_instance, goods_instance)
        order_instance.insurance_fee = float(request.POST.get("claimed_value")) * float(
            request.POST.get("insurance_rate")) / 100
        order_instance.totalPrice = float(order_instance.freight) + float(order_instance.insurance_fee) - \
                                    order_instance.paymentOnAccountFreight + order_instance.packingFee
        order_instance.payable = order_instance.totalPrice - order_instance.paid_price
        order_instance.save()
        # 计算密度
        calculate_density(order_instance, goods_instance)
        order_form.save(freight=order_instance.freight, insurance=order_instance.insurance_fee)
        return render(request, "order/audit/trackorder-audit-modify-complete.html")
    return render(request, "order/audit/trackorder-audit-modify-2.html", {'form': order_form,
                                                                          'good_instance': goods_instance,
                                                                          'order': order_id})


# 生成订单pdf
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def generate_PDF(request, order_id):
    request.session.set_expiry(request.session.get_expiry_age())
    order = get_object_or_404(ShipmentOrder, pk=order_id)
    good = Goods.objects.filter(shipment_order_id_id=order_id)
    ean = barcode.get("Code39", str(order_id), writer=ImageWriter())
    ean.default_writer_options['write_text'] = False
    barcode_img = ean.save("OrderPDF/barcode/" + str(order_id))
    data = {'order': order, 'good': good, 'today': datetime.datetime.now().strftime("%Y-%m-%d"), 'barcode': barcode_img}
    html = get_template('order/pdf.html').render(data)
    file = open("OrderPDF/documents/" + str(order_id) + ".pdf", "w+b")
    pdfmetrics.registerFont(TTFont("yh", os.path.join(settings.DOMAIN_NAME, 'static/fonts/fzlt.ttf')))
    DEFAULT_FONT['helvetica'] = 'yh'
    pisa.CreatePDF(html.encode('utf-8'), dest=file, encoding='utf-8', )
    file.seek(0)
    pdf = file.read()
    file.close()
    return HttpResponse(pdf, 'application/pdf')


# 完成审核 出单
def track_order_audit_finalize(request, order_id):
    request.session.set_expiry(request.session.get_expiry_age())
    order = get_object_or_404(ShipmentOrder, pk=order_id)
    order.status = 2
    order.save()
    return generate_PDF(request, order_id)
