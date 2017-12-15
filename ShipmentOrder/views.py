from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from ShipmentOrder.forms import OrderCreationOneForm, OrderCreationTwoForm, OrderCreationThreeForm, OrderModityForm
from ShipmentOrder.models import ShipmentOrder, Goods
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
import json
import datetime


# 添加订单 第一步 基本信息
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def add_order_stage_one(request):
    if request.method == 'POST':
        form = OrderCreationOneForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.create_date = datetime.datetime.now().strftime("%Y-%m-%d")
            order.handle = request.user
            order.save()
            request.session['draft'] = request.session['draft'] + 1
            request.session['order'] = order.id
            return add_order_stage_two(request, order)
    else:
        form = OrderCreationOneForm()
    return render(request, "order/add/form-addorder-1.html", {'form': form})


# 添加订单 第二步 货物信息显示
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def add_order_stage_two(request, order):
    if "order" not in request.session:
        return render(request, 'error/redirect_error.html')
    form = OrderCreationTwoForm()
    return render(request, "order/add/form-addorder-2.html", {'form': form, 'order': order})


# 添加订单 第二步 货物信息添加 ajax
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def ajax_add_goods(request):
    if "order" not in request.session:
        return render(request, 'error/redirect_error.html')
    form = OrderCreationTwoForm(request.POST)
    order = request.session['order']
    if form.is_valid():
        new_good = Goods(
            shipment_order_id_id=order,
            goods_name=request.POST.get('goods_name'),
            amount=request.POST.get('amount'),
            volume=request.POST.get('volume'),
            weight=request.POST.get('weight'),
            freight=request.POST.get('freight'),
            claim_value=request.POST.get('claim_value'),
            insurance_rate=request.POST.get('insurance_rate'),
            insurance_fee=float(request.POST.get('insurance_rate')) * float(request.POST.get('claim_value')) / 100
        )
        new_good.save()
        good = Goods.objects.filter(shipment_order_id_id=order)
        data = serializers.serialize('json', good)
        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        print(form.errors)


# 添加订单 第二步 货物信息删除
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def ajax_delete_goods(request, good_id):
    if "order" not in request.session:
        return render(request, 'error/redirect_error.html')
    order = request.session['order']
    goods_object = Goods.objects.get(id=good_id)
    goods_object.delete()
    good = Goods.objects.filter(shipment_order_id_id=order)
    data = serializers.serialize('json', good)
    return HttpResponse(json.dumps(data), content_type="application/json")


# 添加订单 第三步骤 页面跳转
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def add_order_stage_three_redirect(request):
    if "order" not in request.session:
        return render(request, 'error/redirect_error.html')
    order = request.session['order']
    order_instance = ShipmentOrder.objects.get(pk=order)
    sum_insurance = 0
    sum_freight = 0

    if request.method == 'POST':
        form = OrderCreationThreeForm(request.POST)
        if form.is_valid():
            order_instance.collectFee = float(request.POST.get('collectFee'))
            order_instance.sendFee = float(request.POST.get("sendFee"))
            order_instance.paymentOnAccountFreight = float(request.POST.get("paymentOnAccountFreight"))
            order_instance.transitFee = float(request.POST.get("transitFee"))
            order_instance.installFee = float(request.POST.get("installFee"))
            order_instance.storeFee = float(request.POST.get("storeFee"))
            order_instance.packingFee = float(request.POST.get("packingFee"))
            order_instance.totalPrice = order_instance.collectFee + order_instance.sendFee + \
                                        float(order_instance.freight) + float(order_instance.insuranceFee) + order_instance.transitFee - \
                                        order_instance.paymentOnAccountFreight + order_instance.installFee + \
                                        order_instance.storeFee + order_instance.packingFee
            order_instance.save()
            return add_order_summary(request)
    else:
        form = OrderCreationThreeForm()
        good = Goods.objects.filter(shipment_order_id_id=order)

        for item in good:
            sum_insurance += item.insurance_fee
            sum_freight += item.freight
        order_instance.insuranceFee = sum_insurance
        order_instance.freight = sum_freight
        order_instance.save()
        return render(request, "order/add/form-addorder-3.html", {'form': form, 'insurance': sum_insurance,
                                                              'freight': sum_freight, 'order': order_instance})


# 添加订单 第四步 信息确认
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def add_order_summary(request):
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
    if "order" not in request.session:
        form_create = OrderCreationOneForm()
        return render(request, "order/add/form-addorder-1.html", {'form': form_create})
    order = request.session['order']
    order_instance = ShipmentOrder.objects.get(pk=order)
    goods_instance = Goods.objects.filter(shipment_order_id_id=order)
    if goods_instance.count() >= 1:
        order_instance.status = 1
        order_instance.save()
        request.session['draft'] = request.session['draft'] - 1
        message = "您的订单已经交由审核"
    else:
        message = "无法提交审核，原因：没有货物。请前往草稿箱修改订单"
    return render(request, "order/add/form-addorder-submitted.html", {'message': message})


# 查询订单 管理端 所有订单
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def track_order_manager(request):
    page = request.GET.get('page')
    order_list = ShipmentOrder.objects.all()
    paginator = Paginator(order_list, 10)
    try:
        order = paginator.page(page)
    except PageNotAnInteger:
        order = paginator.page(1)
    except EmptyPage:
        order = paginator.page(paginator.num_pages)
    return render(request, "order/manage/trackorder-manager.html", {'order': order})


# 查询订单 详情页
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def track_order_detail(request, order_id):
    order = get_object_or_404(ShipmentOrder, pk=order_id)
    good = Goods.objects.filter(shipment_order_id_id=order_id)
    return render(request, "order/manage/trackorder-detail.html", {'order': order, 'good': good})


# 查询订单 编辑页
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def track_order_modify(request, order_id):
    request.session['order_manage'] = order_id
    order_instance = get_object_or_404(ShipmentOrder, id=order_id)
    order_form = OrderModityForm(request.POST or None, instance=order_instance)
    goods_instance = Goods.objects.filter(shipment_order_id_id=order_id)
    goods_form = OrderCreationTwoForm(request.POST or None)

    if order_form.is_valid():
        goods_instance = Goods.objects.filter(shipment_order_id_id=order_id)
        sum_insurance = 0
        sum_freight = 0
        for item in goods_instance:
            sum_insurance += item.insurance_fee
            sum_freight += item.freight
        order_instance.freight = sum_freight
        order_instance.insuranceFee = sum_insurance
        order_form.save(insurance=sum_insurance, freight=sum_freight)
        return render(request, "order/manage/trackorder-modify-complete.html")
    return render(request, "order/manage/trackorder-modify.html", {'form': order_form,
                                                            'good_form': goods_form,
                                                            'good_instance': goods_instance,
                                                            'order': order_id})


# 修改订单 货物信息删除 ajax
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def ajax_delete_goods_manage(request, good_id):
    goods_object = Goods.objects.get(id=good_id)
    goods_object.delete()
    good = Goods.objects.filter(shipment_order_id_id=request.session['order_manage'])
    data = serializers.serialize('json', good)
    return HttpResponse(json.dumps(data), content_type="application/json")


# 修改订单 货物信息添加 ajax
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def ajax_add_goods_manage(request):
    goods_form = OrderCreationTwoForm(request.POST)
    order = request.session['order_manage']
    if goods_form.is_valid():
        new_good = Goods(
            shipment_order_id_id=order,
            goods_name=request.POST.get('goods_name'),
            amount=request.POST.get('amount'),
            volume=request.POST.get('volume'),
            weight=request.POST.get('weight'),
            freight=request.POST.get('freight'),
            claim_value=request.POST.get('claim_value'),
            insurance_rate=request.POST.get('insurance_rate'),
            insurance_fee=float(request.POST.get('insurance_rate')) * float(request.POST.get('claim_value')) / 100
        )
        new_good.save()
        good = Goods.objects.filter(shipment_order_id_id=order)
        data = serializers.serialize('json', good)
        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        print(goods_form.errors)


# 管理订单 确认
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def track_order_confirm_delete(request, order_id):
    order_instance = ShipmentOrder.objects.get(pk=order_id)
    goods_instance = Goods.objects.filter(shipment_order_id_id=order_id)
    return render(request, "order/manage/trackorder-delete-confirm.html", {'order': order_instance, 'good': goods_instance})


# 管理订单 订单删除
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def track_order_delete(request, order_id):
    order_object = get_object_or_404(ShipmentOrder, pk=order_id)
    if order_object.handle == request.user and order_object.status == 0:
        request.session['draft'] = request.session['draft'] - 1
    order_object.delete()
    return render(request, "order/manage/trackorder-delete-complete.html")


# 管理订单 订单搜索
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def track_order_search(request):
    query = request.GET.get('query')
    page = request.GET.get('page')
    result = ShipmentOrder.objects.filter(
        Q(sender__icontains=query)|
        Q(from_address__icontains=query)|
        Q(sender_contact__icontains=query)|
        Q(receiver__icontains=query)|
        Q(to_address__icontains=query)|
        Q(receiver_contact__icontains=query)|
        Q(mode__icontains=query)|
        Q(comments__icontains=query))
    paginator = Paginator(result, 10)
    try:
        order = paginator.page(page)
    except PageNotAnInteger:
        order = paginator.page(1)
    except EmptyPage:
        order = paginator.page(paginator.num_pages)
    return render(request, "order/manage/trackorder-manager.html", {'order': order, 'query': query})


@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def track_order_search_advanced(request):
    return render(request, "order/search/trackorder-search.html")


# 管理订单 订单搜索结果
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def track_order_search_advanced_result(request):
    keyword = request.GET.get('keyword')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    status = request.GET.get('status')
    page = request.GET.get('page')
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

    paginator = Paginator(result, 10)
    try:
        order = paginator.page(page)
    except PageNotAnInteger:
        order = paginator.page(1)
    except EmptyPage:
        order = paginator.page(paginator.num_pages)
    return render(request, "order/search/trackorder-search-result.html", {'order': order,
                                                                   'keyword': keyword,
                                                                   'start_date': start_date,
                                                                   'end_date': end_date,
                                                                   'status': status})


# 管理订单 草稿箱
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def track_order_draft(request):
    page = request.GET.get('page')
    order_list = ShipmentOrder.objects.filter(handle=request.user, status=0)
    paginator = Paginator(order_list, 10)
    try:
        order = paginator.page(page)
    except PageNotAnInteger:
        order = paginator.page(1)
    except EmptyPage:
        order = paginator.page(paginator.num_pages)
    return render(request, "order/draft/trackorder-draft.html", {'order': order})


# 管理订单 草稿箱 编辑
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def track_order_draft_modify(request, order_id):
    request.session['order_manage'] = order_id
    order_instance = get_object_or_404(ShipmentOrder, id=order_id)
    order_form = OrderModityForm(request.POST or None, instance=order_instance)
    goods_instance = Goods.objects.filter(shipment_order_id_id=order_id)
    goods_form = OrderCreationTwoForm(request.POST or None)

    if order_form.is_valid():
        goods_instance = Goods.objects.filter(shipment_order_id_id=order_id)
        sum_insurance = 0
        sum_freight = 0
        for item in goods_instance:
            sum_insurance += item.insurance_fee
            sum_freight += item.freight
        order_instance.freight = sum_freight
        order_instance.insuranceFee = sum_insurance
        order_form.save(insurance=sum_insurance, freight=sum_freight)
        return render(request, "order/draft/trackorder-draft-modify-complete.html")
    return render(request, "order/draft/trackorder-draft-modify.html", {'form': order_form,
                                                                        'good_form': goods_form,
                                                                        'good_instance': goods_instance,
                                                                        'order': order_id})


# 管理订单 提交审核
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def track_order_submit_audit(request, order_id):
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
    page = request.GET.get('page')
    order_list = ShipmentOrder.objects.filter(status=1)
    paginator = Paginator(order_list, 10)
    try:
        order = paginator.page(page)
    except PageNotAnInteger:
        order = paginator.page(1)
    except EmptyPage:
        order = paginator.page(paginator.num_pages)
    return render(request, "order/audit/trackorder-audit.html", {'order': order})