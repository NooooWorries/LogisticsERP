from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from ShipmentOrder.forms import OrderCreationOneForm, OrderCreationTwoForm
from ShipmentOrder.models import ShipmentOrder, Goods
from django.core import serializers
import json


# 添加订单 第一步 基本信息
@csrf_exempt
def add_order_stage_one(request):
    if request.method == 'POST':
        form = OrderCreationOneForm(request.POST)
        form_two = OrderCreationTwoForm(request.POST)
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