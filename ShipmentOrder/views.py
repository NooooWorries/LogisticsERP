from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from ShipmentOrder.forms import OrderCreationOneForm, OrderCreationTwoForm, OrderCreationThreeForm
from ShipmentOrder.models import ShipmentOrder, Goods
from django.core import serializers
import json


# 添加订单 第一步 基本信息
@csrf_exempt
def add_order_stage_one(request):
    if request.method == 'POST':
        form = OrderCreationOneForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            return add_order_stage_two(request, order)
    else:
        form = OrderCreationOneForm()
    return render(request, "order/form-addorder-1.html", {'form': form})


# 添加订单 第二步 货物信息显示
@csrf_exempt
def add_order_stage_two(request, order):
    form = OrderCreationTwoForm()
    request.session['order'] = order.id
    return render(request, "order/form-addorder-2.html", {'form': form, 'order': order})


# 添加订单 第二步 货物信息添加 ajax
@csrf_exempt
def ajax_add_goods(request):
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
def ajax_delete_goods(request, good_id):
    order = request.session['order']
    goods_object = Goods.objects.get(id=good_id)
    goods_object.delete()
    good = Goods.objects.filter(shipment_order_id_id=order)
    data = serializers.serialize('json', good)
    return HttpResponse(json.dumps(data), content_type="application/json")


# 添加订单 第三步骤 页面跳转
@csrf_exempt
def add_order_stage_three_redirect(request):
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
def add_order_summary(request):
    order = request.session['order']
    order_instance = ShipmentOrder.objects.get(pk=order)
    goods_instance = Goods.objects.filter(shipment_order_id_id=order)
    return render(request, "order/form-addorder-summary.html", {'order': order_instance, 'good': goods_instance})


# 添加订单 第五步 交由审核
@csrf_exempt
def add_order_audit(request):
    order = request.session['order']
    order_instance = ShipmentOrder.objects.get(pk=order)
    order_instance.status = 1
    return render(request, "order/form-addorder-submitted.html")

