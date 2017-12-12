from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from ShipmentOrder.forms import OrderCreationOneForm, OrderCreationTwoForm, OrderCreationThreeForm
from ShipmentOrder.models import ShipmentOrder, Goods
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
            request.session['order'] = order.id
            return add_order_stage_two(request, order)
    else:
        form = OrderCreationOneForm()
    return render(request, "order/form-addorder-1.html", {'form': form})


# 添加订单 第二步 货物信息显示
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def add_order_stage_two(request, order):
    if "order" not in request.session:
        form_create = OrderCreationOneForm()
        return render(request, "order/form-addorder-1.html", {'form': form_create})
    form = OrderCreationTwoForm()
    return render(request, "order/form-addorder-2.html", {'form': form, 'order': order})


# 添加订单 第二步 货物信息添加 ajax
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def ajax_add_goods(request):
    if "order" not in request.session:
        form_create = OrderCreationOneForm()
        return render(request, "order/form-addorder-1.html", {'form': form_create})
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
        form_create = OrderCreationOneForm()
        return render(request, "order/form-addorder-1.html", {'form': form_create})
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
        form_create = OrderCreationOneForm()
        return render(request, "order/form-addorder-1.html", {'form': form_create})
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
        return render(request, "order/form-addorder-3.html", {'form': form, 'insurance': sum_insurance,
                                                              'freight': sum_freight, 'order': order_instance})


# 添加订单 第四步 信息确认
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def add_order_summary(request):
    if "order" not in request.session:
        form_create = OrderCreationOneForm()
        return render(request, "order/form-addorder-1.html", {'form': form_create})
    order = request.session['order']
    order_instance = ShipmentOrder.objects.get(pk=order)
    goods_instance = Goods.objects.filter(shipment_order_id_id=order)
    return render(request, "order/form-addorder-summary.html", {'order': order_instance, 'good': goods_instance})


# 添加订单 第五步 交由审核
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def add_order_audit(request):
    if "order" not in request.session:
        form_create = OrderCreationOneForm()
        return render(request, "order/form-addorder-1.html", {'form': form_create})
    order = request.session['order']
    order_instance = ShipmentOrder.objects.get(pk=order)
    goods_instance = Goods.objects.filter(shipment_order_id_id=order)
    message = ""
    if goods_instance.count() >= 1:
        order_instance.status = 1
        message = "您的订单已经交由审核"
    else:
        message = "无法提交审核，原因：没有货物。请前往草稿箱修改订单"
    return render(request, "order/form-addorder-submitted.html", {'message': message})


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
    return render(request, "order/trackorder-manager.html", {'order': order})


# 查询订单 管理端 未提交
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def track_order_manager(request):
    page = request.GET.get('page')
    order_list = ShipmentOrder.objects.filter(status=0)
    paginator = Paginator(order_list, 10)
    try:
        order = paginator.page(page)
    except PageNotAnInteger:
        order = paginator.page(1)
    except EmptyPage:
        order = paginator.page(paginator.num_pages)
    return render(request, "order/trackorder-manager.html", {'order': order})


# 查询订单 管理端 待审核
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def track_order_manager(request):
    page = request.GET.get('page')
    order_list = ShipmentOrder.objects.filter(status=1)
    paginator = Paginator(order_list, 10)
    try:
        order = paginator.page(page)
    except PageNotAnInteger:
        order = paginator.page(1)
    except EmptyPage:
        order = paginator.page(paginator.num_pages)
    return render(request, "order/trackorder-manager.html", {'order': order})


# 查询订单 管理端 审核通过
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def track_order_manager(request):
    page = request.GET.get('page')
    order_list = ShipmentOrder.objects.filter(status=2)
    paginator = Paginator(order_list, 10)
    try:
        order = paginator.page(page)
    except PageNotAnInteger:
        order = paginator.page(1)
    except EmptyPage:
        order = paginator.page(paginator.num_pages)
    return render(request, "order/trackorder-manager.html", {'order': order})


# 查询订单 管理端 已完成
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def track_order_manager(request):
    page = request.GET.get('page')
    order_list = ShipmentOrder.objects.filter(status=3)
    paginator = Paginator(order_list, 10)
    try:
        order = paginator.page(page)
    except PageNotAnInteger:
        order = paginator.page(1)
    except EmptyPage:
        order = paginator.page(paginator.num_pages)
    return render(request, "order/trackorder-manager.html", {'order': order})