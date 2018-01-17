from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from ShipmentOrder.models import ShipmentOrder
from Dispatch.models import DispatchRecord
from Finance.models import PaymentOrder
from django.db.models import Q
import datetime


@login_required(login_url='/error/not-logged-in/')
def index(request):
    request.session.set_expiry(request.session.get_expiry_age())
    # 统计数据
    # 时间域
    time = [None] * 7
    for i in range(7):
        time[i] = (datetime.datetime.now() - datetime.timedelta(days=7 - i)).strftime("%Y-%m-%d")
    # 数据
    shipment_order_count = ShipmentOrder.objects.filter(Q(create_date__range=(time[0], time[6]))).count()
    dispatch_order_count = DispatchRecord.objects.filter(Q(dispatch_date__range=(time[0], time[6]))).count()
    payment_order_list = PaymentOrder.objects.filter(Q(payment_date__range=(time[0], time[6])))
    payment_order_count = payment_order_list.count()
    payment_amount = 0
    for item in payment_order_list:
        payment_amount = payment_amount + item.amount


    return render(request, 'index.html', {'shipment_order_count': shipment_order_count,
                                          'dispatch_order_count': dispatch_order_count,
                                          'payment_order_count': payment_order_count,
                                          'payment_amount': round(payment_amount, 2)})


def error_404(request):
    request.session.set_expiry(request.session.get_expiry_age())
    data = {}
    return render(request, 'error/404.html', data)


def error_500(request):
    request.session.set_expiry(request.session.get_expiry_age())
    data = {}
    return render(request, 'error/500.html', data)


def error_not_logged_in(request):
    request.session.set_expiry(request.session.get_expiry_age())
    data = {}
    return render(request, 'error/not-logged-in.html', data)


def error_redirect(request):
    request.session.set_expiry(request.session.get_expiry_age())
    data = {}
    return render(request, 'error/redirect_error.html', data)
