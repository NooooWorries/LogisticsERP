from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from ShipmentOrder.models import ShipmentOrder
from Customers.models import Customer, CustomerClass
from Dispatch.models import DispatchRecord
from django.db.models import Q
import datetime
import json


@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def order_diagram(request):
    request.session.set_expiry(request.session.get_expiry_age())
    return render(request, "diagram/diagram-order.html")


@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def ajax_order_weekly(request):
    request.session.set_expiry(request.session.get_expiry_age())
    # 时间域
    time = [None] * 7
    for i in range(7):
        time[i] = (datetime.datetime.now() - datetime.timedelta(days=7-i)).strftime("%Y-%m-%d")
    # 草稿数量
    draft = [None] * 7
    for i in range(7):
        draft[i] = ShipmentOrder.objects.filter(Q(create_date__exact=time[i]) & Q(status__exact=0)).count()
    # 未审核数量
    non_audit = [None] * 7
    for i in range(7):
        non_audit[i] = ShipmentOrder.objects.filter(Q(create_date__exact=time[i]) & Q(status__exact=1)).count()
    # 已审核数量
    audited = [None] * 7
    for i in range(7):
        audited[i] = ShipmentOrder.objects.filter(Q(create_date__exact=time[i]) & Q(status__exact=2)).count()
    # 已完成数量
    finished = [None] * 7
    for i in range(7):
        finished[i] = ShipmentOrder.objects.filter(Q(create_date__exact=time[i]) & Q(status__exact=3)).count()
    data = json.dumps({
        'time': time,
        'draft': draft,
        'non_audit': non_audit,
        'audited': audited,
        'finished': finished,
        'start': time[0],
        'end': time[6]
    })
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def ajax_order_monthly(request):
    request.session.set_expiry(request.session.get_expiry_age())
    # 时间域
    time = [None] * 4
    time_start = [None] * 4
    time_end = [None] * 4
    for i in range(4):
        time_start[i] = (datetime.datetime.now() - datetime.timedelta(days=7*(4-i))).strftime("%Y-%m-%d")
        time_end[i] = (datetime.datetime.now() - datetime.timedelta(days=7*(4-i-1)+1)).strftime("%Y-%m-%d")
        time[i] = (datetime.datetime.now() - datetime.timedelta(days=7*(4-i))).strftime("%m-%d") + \
                  " 到 " +(datetime.datetime.now() - datetime.timedelta(days=7*(4-i-1)+1)).strftime("%m-%d")
    # 草稿数量
    draft = [None] * 4
    for i in range(4):
        draft[i] = ShipmentOrder.objects.filter(
            Q(create_date__range=(time_start[i], time_end[i])) &
            Q(status__exact=0)
        ).count()
    # 未审核数量
    non_audit = [None] * 4
    for i in range(4):
        non_audit[i] = ShipmentOrder.objects.filter(
            Q(create_date__range=(time_start[i], time_end[i])) &
            Q(status__exact=1)
        ).count()
    # 已审核数量
    audited = [None] * 4
    for i in range(4):
        audited[i] = ShipmentOrder.objects.filter(
            Q(create_date__range=(time_start[i], time_end[i])) &
            Q(status__exact=2)
        ).count()
    # 已完成数量
    finished = [None] * 4
    for i in range(4):
        finished[i] = ShipmentOrder.objects.filter(
            Q(create_date__range=(time_start[i], time_end[i])) &
            Q(status__exact=3)
        ).count()
    data = json.dumps({
        'time': time,
        'draft': draft,
        'non_audit': non_audit,
        'audited': audited,
        'finished': finished,
        'start': time_start[0],
        'end': time_end[3]
    })
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def ajax_order_yearly(request):
    request.session.set_expiry(request.session.get_expiry_age())
    # 时间域
    time = [None] * 12
    time_year = [None] * 12
    time_month = [None] * 12
    for i in range(12):
        time[i] = (datetime.datetime.now() - datetime.timedelta((12-i)*365/12)).strftime("%Y-%m")
        time_year[i] = (datetime.datetime.now() - datetime.timedelta((12-i)*365/12)).strftime("%Y")
        time_month[i] = (datetime.datetime.now() - datetime.timedelta((12 - i) * 365 / 12)).strftime("%m")
    # 草稿数量
    draft = [None] * 12
    for i in range(12):
        draft[i] = ShipmentOrder.objects.filter(Q(create_date__month=time_month[i]) &
                                                Q(create_date__year=time_year[i]) &
                                                Q(status__exact=0)).count()
    # 未审核数量
    non_audit = [None] * 12
    for i in range(12):
        non_audit[i] = ShipmentOrder.objects.filter(Q(create_date__month=time_month[i]) &
                                                    Q(create_date__year=time_year[i]) &
                                                    Q(status__exact=1)).count()
    # 已审核数量
    audited = [None] * 12
    for i in range(12):
        audited[i] = ShipmentOrder.objects.filter(Q(create_date__month=time_month[i]) &
                                                  Q(create_date__year=time_year[i]) &
                                                  Q(status__exact=2)).count()
    # 已完成数量
    finished = [None] * 12
    for i in range(12):
        finished[i] = ShipmentOrder.objects.filter(Q(create_date__month=time_month[i]) &
                                                   Q(create_date__year=time_year[i]) &
                                                   Q(status__exact=3)).count()
    data = json.dumps({
        'time': time,
        'draft': draft,
        'non_audit': non_audit,
        'audited': audited,
        'finished': finished,
        'start': time[0],
        'end': time[11]
    })
    return HttpResponse(data, content_type='application/json')