import json
from django.http import HttpResponse
from django.core import serializers

from _datetime import datetime
from django.shortcuts import get_object_or_404
from django.shortcuts import render, render_to_response
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.db.models import Q

from ShipmentOrder.forms import OrderCreationOneForm


@csrf_exempt
# 添加订单 第一步 基本信息
def add_order_stage_one(request):
    if request.method == 'POST':
        form = OrderCreationOneForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            return HttpResponse("Success");
    else:
        form = OrderCreationOneForm()
    return render(request, "order/form-addorder-1.html", {'form': form})