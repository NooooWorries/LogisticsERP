from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from ShipmentOrder.models import ShipmentOrder
from Finance.models import PaymentOrder
from Dispatch.models import DispatchRecord
from django.db.models import Q

from collections import OrderedDict
import datetime
import json
import pandas as pd


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


@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def ajax_order_customize(request):
    request.session.set_expiry(request.session.get_expiry_age())
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date is "": start_date = ShipmentOrder.objects.all().order_by('create_date')[0].create_date.strftime("%Y-%m-%d")
    if end_date is "": end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    start = start_date
    end = end_date
    # 时间段生成
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    interval = (end_date - start_date).days

    if interval <= 14:
        time = [None] * (interval + 1)
        for i in range(interval + 1):
            time[i] = (end_date - datetime.timedelta(days=interval - i)).strftime("%Y-%m-%d")
            # 过滤数据与生成
            # 草稿数量
            draft = [None] * interval
            for i in range(interval):
                draft[i] = ShipmentOrder.objects.filter(Q(create_date__exact=time[i]) & Q(status__exact=0)).count()
            # 未审核数量
            non_audit = [None] * interval
            for i in range(interval):
                non_audit[i] = ShipmentOrder.objects.filter(Q(create_date__exact=time[i]) & Q(status__exact=1)).count()
            # 已审核数量
            audited = [None] * interval
            for i in range(interval):
                audited[i] = ShipmentOrder.objects.filter(Q(create_date__exact=time[i]) & Q(status__exact=2)).count()
            # 已完成数量
            finished = [None] * interval
            for i in range(interval):
                finished[i] = ShipmentOrder.objects.filter(Q(create_date__exact=time[i]) & Q(status__exact=3)).count()

    elif interval <= 84:
        gap = int(interval / 7)
        num_of_object = interval / 7
        if interval % 7 is 0:
            num_of_object = int(num_of_object)
        else:
            num_of_object = int(num_of_object) + 1
        time = [None] * num_of_object
        time_start = [None] * num_of_object
        time_end = [None] * num_of_object

        start = time_start[0]
        end = time_end[len(time_end) - 1]

        for i in range(gap):
            time_start[i] = (start_date + datetime.timedelta(days=7 * i)).strftime("%Y-%m-%d")
            time_end[i] = (start_date + datetime.timedelta(days=7 * (i + 1) - 1)).strftime("%Y-%m-%d")
            time[i] = time_start[i] + " 到 " + time_end[i]
        if(interval % 7) is not 0:
            time_start[num_of_object-1] = (end_date - datetime.timedelta(days=interval % 7)).strftime("%Y-%m-%d")
            time_end[num_of_object-1] = end_date.strftime("%Y-%m-%d")
            time[num_of_object-1] = time_start[num_of_object-1] + " 到 " + time_end[num_of_object-1]
            # 草稿数量
        draft = [None] * num_of_object
        for i in range(num_of_object):
            draft[i] = ShipmentOrder.objects.filter(
                Q(create_date__range=(time_start[i], time_end[i])) &
                Q(status__exact=0)
            ).count()
        # 未审核数量
        non_audit = [None] * num_of_object
        for i in range(num_of_object):
            non_audit[i] = ShipmentOrder.objects.filter(
                Q(create_date__range=(time_start[i], time_end[i])) &
                Q(status__exact=1)
            ).count()
        # 已审核数量
        audited = [None] * num_of_object
        for i in range(num_of_object):
            audited[i] = ShipmentOrder.objects.filter(
                Q(create_date__range=(time_start[i], time_end[i])) &
                Q(status__exact=2)
            ).count()
        # 已完成数量
        finished = [None] * num_of_object
        for i in range(num_of_object):
            finished[i] = ShipmentOrder.objects.filter(
                Q(create_date__range=(time_start[i], time_end[i])) &
                Q(status__exact=3)
            ).count()

    else:
        time = pd.date_range(start_date, end_date, freq='1M')
        time = time.union([time[-1] + 1])
        time_year = time.union([time[-1] + 1])
        time_month = time.union([time[-1] + 1])
        time = [d.strftime("%Y-%m") for d in time]
        time_year = [d.strftime("%Y") for d in time_year]
        time_month = [d.strftime("%m") for d in time_month]
        num_of_object = len(time)
        # 草稿数量
        draft = [None] * num_of_object
        for i in range(num_of_object):
            draft[i] = ShipmentOrder.objects.filter(Q(create_date__month=time_month[i]) &
                                                    Q(create_date__year=time_year[i]) &
                                                    Q(status__exact=0)).count()
        # 未审核数量
        non_audit = [None] * num_of_object
        for i in range(num_of_object):
            non_audit[i] = ShipmentOrder.objects.filter(Q(create_date__month=time_month[i]) &
                                                        Q(create_date__year=time_year[i]) &
                                                        Q(status__exact=1)).count()
        # 已审核数量
        audited = [None] * num_of_object
        for i in range(num_of_object):
            audited[i] = ShipmentOrder.objects.filter(Q(create_date__month=time_month[i]) &
                                                      Q(create_date__year=time_year[i]) &
                                                      Q(status__exact=2)).count()
        # 已完成数量
        finished = [None] * num_of_object
        for i in range(num_of_object):
            finished[i] = ShipmentOrder.objects.filter(Q(create_date__month=time_month[i]) &
                                                       Q(create_date__year=time_year[i]) &
                                                       Q(status__exact=3)).count()
        start = time[0]
        end = time[len(time)-1]
    data = json.dumps({
        'time': time,
        'draft': draft,
        'non_audit': non_audit,
        'audited': audited,
        'finished': finished,
        'start': start,
        'end': end
    })
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def dispatch_order_diagram(request):
    request.session.set_expiry(request.session.get_expiry_age())
    return render(request, "diagram/diagram-dispatch-order.html")


@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def ajax_dispatch_order_weekly(request):
    request.session.set_expiry(request.session.get_expiry_age())
    # 时间域
    time = [None] * 7
    for i in range(7):
        time[i] = (datetime.datetime.now() - datetime.timedelta(days=7-i)).strftime("%Y-%m-%d")
    # 草稿数量
    draft = [None] * 7
    for i in range(7):
        draft[i] = DispatchRecord.objects.filter(Q(dispatch_date__exact=time[i]) & Q(status__exact=0)).count()
    # 已出车数量
    dispatched = [None] * 7
    for i in range(7):
        dispatched[i] = DispatchRecord.objects.filter(Q(dispatch_date__exact=time[i]) & Q(status__exact=1)).count()
    # 已完成数量
    finished = [None] * 7
    for i in range(7):
        finished[i] = DispatchRecord.objects.filter(Q(dispatch_date__exact=time[i]) & Q(status__exact=2)).count()
    data = json.dumps({
        'time': time,
        'draft': draft,
        'dispatched': dispatched,
        'finished': finished,
        'start': time[0],
        'end': time[6]
    })
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def ajax_dispatch_order_monthly(request):
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
        draft[i] = DispatchRecord.objects.filter(
            Q(dispatch_date__range=(time_start[i], time_end[i])) &
            Q(status__exact=0)
        ).count()
    # 已出车
    dispatched = [None] * 4
    for i in range(4):
        dispatched[i] = DispatchRecord.objects.filter(
            Q(dispatch_date__range=(time_start[i], time_end[i])) &
            Q(status__exact=1)
        ).count()
    # 已完成数量
    finished = [None] * 4
    for i in range(4):
        finished[i] = DispatchRecord.objects.filter(
            Q(dispatch_date__range=(time_start[i], time_end[i])) &
            Q(status__exact=2)
        ).count()
    data = json.dumps({
        'time': time,
        'draft': draft,
        'dispatched': dispatched,
        'finished': finished,
        'start': time_start[0],
        'end': time_end[3]
    })
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def ajax_dispatch_order_yearly(request):
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
        draft[i] = DispatchRecord.objects.filter(Q(dispatch_date__month=time_month[i]) &
                                                Q(dispatch_date__year=time_year[i]) &
                                                Q(status__exact=0)).count()
    # 未审核数量
    dispatched = [None] * 12
    for i in range(12):
        dispatched[i] = DispatchRecord.objects.filter(Q(dispatch_date__month=time_month[i]) &
                                                    Q(dispatch_date__year=time_year[i]) &
                                                    Q(status__exact=1)).count()
    # 已完成数量
    finished = [None] * 12
    for i in range(12):
        finished[i] = DispatchRecord.objects.filter(Q(dispatch_date__month=time_month[i]) &
                                                   Q(dispatch_date__year=time_year[i]) &
                                                   Q(status__exact=2)).count()
    data = json.dumps({
        'time': time,
        'draft': draft,
        'dispatched': dispatched,
        'finished': finished,
        'start': time[0],
        'end': time[11]
    })
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def ajax_dispatch_order_customize(request):
    request.session.set_expiry(request.session.get_expiry_age())
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date is "": start_date = DispatchRecord.objects.all().order_by('dispatch_date')[0].dispatch_date.strftime("%Y-%m-%d")
    if end_date is "": end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    start = start_date
    end = end_date

    # 时间段生成
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    interval = (end_date - start_date).days

    if interval <= 14:
        time = [None] * (interval + 1)
        start = time[0]
        end = time[interval-1]
        for i in range(interval + 1):
            time[i] = (end_date - datetime.timedelta(days=interval - i)).strftime("%Y-%m-%d")
            # 过滤数据与生成
            # 草稿数量
            draft = [None] * interval
            for i in range(interval):
                draft[i] = DispatchRecord.objects.filter(Q(dispatch_date__exact=time[i]) & Q(status__exact=0)).count()
            # 已出车数量
            dispatched = [None] * interval
            for i in range(interval):
                dispatched[i] = DispatchRecord.objects.filter(
                    Q(dispatch_date__exact=time[i]) & Q(status__exact=1)).count()
            # 已完成数量
            finished = [None] * interval
            for i in range(interval):
                finished[i] = DispatchRecord.objects.filter(
                    Q(dispatch_date__exact=time[i]) & Q(status__exact=2)).count()

    elif interval <= 84:
        gap = int(interval / 7)
        num_of_object = interval / 7
        if interval % 7 is 0:
            num_of_object = int(num_of_object)
        else:
            num_of_object = int(num_of_object) + 1
        time = [None] * num_of_object
        time_start = [None] * num_of_object
        time_end = [None] * num_of_object

        for i in range(gap):
            time_start[i] = (start_date + datetime.timedelta(days=7 * i)).strftime("%Y-%m-%d")
            time_end[i] = (start_date + datetime.timedelta(days=7 * (i + 1) - 1)).strftime("%Y-%m-%d")
            time[i] = time_start[i] + " 到 " + time_end[i]
        if(interval % 7) is not 0:
            time_start[num_of_object-1] = (end_date - datetime.timedelta(days=interval % 7)).strftime("%Y-%m-%d")
            time_end[num_of_object-1] = end_date.strftime("%Y-%m-%d")
            time[num_of_object-1] = time_start[num_of_object-1] + " 到 " + time_end[num_of_object-1]
        # 草稿数量
        draft = [None] * num_of_object
        for i in range(num_of_object):
            draft[i] = DispatchRecord.objects.filter(
                Q(dispatch_date__range=(time_start[i], time_end[i])) &
                Q(status__exact=0)
            ).count()
        # 已出车
        dispatched = [None] * num_of_object
        for i in range(num_of_object):
            dispatched[i] = DispatchRecord.objects.filter(
                 Q(dispatch_date__range=(time_start[i], time_end[i])) &
                 Q(status__exact=1)
             ).count()
        # 已完成数量
        finished = [None] * num_of_object
        for i in range(num_of_object):
             finished[i] = DispatchRecord.objects.filter(
                 Q(dispatch_date__range=(time_start[i], time_end[i])) &
                 Q(status__exact=2)
              ).count()
        start = time_start[0]
        end = time_end[len(time_end)-1]
    else:
        time = pd.date_range(start_date, end_date, freq='1M')
        time = time.union([time[-1] + 1])
        time_year = time.union([time[-1] + 1])
        time_month = time.union([time[-1] + 1])
        time = [d.strftime("%Y-%m") for d in time]
        time_year = [d.strftime("%Y") for d in time_year]
        time_month = [d.strftime("%m") for d in time_month]
        num_of_object = len(time)
        # 草稿数量
        draft = [None] * num_of_object
        for i in range(num_of_object):
            draft[i] = DispatchRecord.objects.filter(Q(dispatch_date__month=time_month[i]) &
                                                     Q(dispatch_date__year=time_year[i]) &
                                                     Q(status__exact=0)).count()
        # 未审核数量
        dispatched = [None] * num_of_object
        for i in range(num_of_object):
            dispatched[i] = DispatchRecord.objects.filter(Q(dispatch_date__month=time_month[i]) &
                                                          Q(dispatch_date__year=time_year[i]) &
                                                          Q(status__exact=1)).count()
        # 已完成数量
        finished = [None] * num_of_object
        for i in range(num_of_object):
            finished[i] = DispatchRecord.objects.filter(Q(dispatch_date__month=time_month[i]) &
                                                        Q(dispatch_date__year=time_year[i]) &
                                                        Q(status__exact=2)).count()
        start = time[0]
        end = time[len(time)-1]
    data = json.dumps({
        'time': time,
        'draft': draft,
        'dispatched': dispatched,
        'finished': finished,
        'start': start,
        'end': end
    })
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def payment_order_diagram(request):
    request.session.set_expiry(request.session.get_expiry_age())
    return render(request, "diagram/diagram-payment-order.html")


@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def ajax_payment_order_weekly(request):
    request.session.set_expiry(request.session.get_expiry_age())
    # 时间域
    time = [None] * 7
    for i in range(7):
        time[i] = (datetime.datetime.now() - datetime.timedelta(days=7-i)).strftime("%Y-%m-%d")

    amount = [None] * 7
    count = [None] * 7
    for i in range(7):
        count[i] = PaymentOrder.objects.filter(Q(payment_date__exact=time[i])).count()
        object_list = PaymentOrder.objects.filter(Q(payment_date__exact=time[i]))
        sum = 0
        for item in object_list:
            sum = sum + item.amount
        amount[i] = sum

    data = json.dumps({
        'time': time,
        'amount': amount,
        'count': count,
        'start': time[0],
        'end': time[6]
    })
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def ajax_payment_order_monthly(request):
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

    amount = [None] * 4
    count = [None] * 4
    for i in range(4):
        count[i] = PaymentOrder.objects.filter(Q(payment_date__range=(time_start[i], time_end[i]))).count()
        object_list = PaymentOrder.objects.filter(Q(payment_date__range=(time_start[i], time_end[i])))
        sum = 0
        for item in object_list:
            sum = sum + item.amount
        amount[i] = sum

    data = json.dumps({
        'time': time,
        'amount': amount,
        'count': count,
        'start': time_start[0],
        'end': time_end[3]
    })
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def ajax_payment_order_yearly(request):
    request.session.set_expiry(request.session.get_expiry_age())
    # 时间域
    time = [None] * 12
    time_year = [None] * 12
    time_month = [None] * 12
    for i in range(12):
        time[i] = (datetime.datetime.now() - datetime.timedelta((12-i)*365/12)).strftime("%Y-%m")
        time_year[i] = (datetime.datetime.now() - datetime.timedelta((12-i)*365/12)).strftime("%Y")
        time_month[i] = (datetime.datetime.now() - datetime.timedelta((12 - i) * 365 / 12)).strftime("%m")

    amount = [None] * 12
    count = [None] * 12
    for i in range(12):
        count[i] = PaymentOrder.objects.filter(Q(payment_date__month=time_month[i]) &
                                               Q(payment_date__year=time_year[i])).count()
        object_list = PaymentOrder.objects.filter(Q(payment_date__month=time_month[i]) &
                                                  Q(payment_date__year=time_year[i]))
        sum = 0
        for item in object_list:
            sum = sum + item.amount
        amount[i] = sum

    data = json.dumps({
        'time': time,
        'amount': amount,
        'count': count,
        'start': time[0],
        'end': time[11]
    })
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def ajax_payment_order_customize(request):
    request.session.set_expiry(request.session.get_expiry_age())
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date is "": start_date = DispatchRecord.objects.all().order_by('dispatch_date')[0].dispatch_date.strftime("%Y-%m-%d")
    if end_date is "": end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    start = start_date
    end = end_date

    # 时间段生成
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    interval = (end_date - start_date).days

    if interval <= 14:
        time = [None] * (interval + 1)
        for i in range(interval + 1):
            time[i] = (end_date - datetime.timedelta(days=interval - i)).strftime("%Y-%m-%d")
            # 过滤数据与生成
            amount = [None] * interval
            count = [None] * interval
            for i in range(interval):
                count[i] = PaymentOrder.objects.filter(Q(payment_date__exact=time[i])).count()
                object_list = PaymentOrder.objects.filter(Q(payment_date__exact=time[i]))
                sum = 0
                for item in object_list:
                    sum = sum + item.amount
                amount[i] = sum

    elif interval <= 84:
        gap = int(interval / 7)
        num_of_object = interval / 7
        if interval % 7 is 0:
            num_of_object = int(num_of_object)
        else:
            num_of_object = int(num_of_object) + 1
        time = [None] * num_of_object
        time_start = [None] * num_of_object
        time_end = [None] * num_of_object

        for i in range(gap):
            time_start[i] = (start_date + datetime.timedelta(days=7 * i)).strftime("%Y-%m-%d")
            time_end[i] = (start_date + datetime.timedelta(days=7 * (i + 1) - 1)).strftime("%Y-%m-%d")
            time[i] = time_start[i] + " 到 " + time_end[i]
        if(interval % 7) is not 0:
            time_start[num_of_object-1] = (end_date - datetime.timedelta(days=interval % 7)).strftime("%Y-%m-%d")
            time_end[num_of_object-1] = end_date.strftime("%Y-%m-%d")
            time[num_of_object-1] = time_start[num_of_object-1] + " 到 " + time_end[num_of_object-1]

        amount = [None] * num_of_object
        count = [None] * num_of_object
        for i in range(num_of_object):
            count[i] = PaymentOrder.objects.filter(Q(payment_date__range=(time_start[i], time_end[i]))).count()
            object_list = PaymentOrder.objects.filter(Q(payment_date__range=(time_start[i], time_end[i])))
            sum = 0
            for item in object_list:
                sum = sum + item.amount
            amount[i] = sum

        start = time_start[0]
        end = time_end[len(time_end)-1]
    else:
        time = pd.date_range(start_date, end_date, freq='1M')
        time = time.union([time[-1] + 1])
        time_year = time.union([time[-1] + 1])
        time_month = time.union([time[-1] + 1])
        time = [d.strftime("%Y-%m") for d in time]
        time_year = [d.strftime("%Y") for d in time_year]
        time_month = [d.strftime("%m") for d in time_month]
        num_of_object = len(time)

        amount = [None] * num_of_object
        count = [None] * num_of_object
        for i in range(num_of_object):
            count[i] = PaymentOrder.objects.filter(Q(payment_date__month=time_month[i]) &
                                                   Q(payment_date__year=time_year[i])).count()
            object_list = PaymentOrder.objects.filter(Q(payment_date__month=time_month[i]) &
                                                      Q(payment_date__year=time_year[i]))
            sum = 0
            for item in object_list:
                sum = sum + item.amount
            amount[i] = sum

        start = time[0]
        end = time[len(time)-1]
    data = json.dumps({
        'time': time,
        'amount': amount,
        'count': count,
        'start': start,
        'end': end
    })
    return HttpResponse(data, content_type='application/json')