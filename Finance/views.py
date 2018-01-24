from django.shortcuts import render, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from ShipmentOrder.models import ShipmentOrder
from Finance.models import PaymentOrder
from Finance.forms import PaymentOrderCreationForm
from django.db.models import Q
from LogisticsERP import settings, utils
from decimal import Decimal
import datetime


# 选择订单
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def receivable_list(request):
    request.session.set_expiry(request.session.get_expiry_age())
    role = utils.get_user_type(request)
    if role != 0 and role != 4:
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
    order_list = ShipmentOrder.objects.filter(status=3, payable__gt=0.01).order_by("-create_date")[startPos:endPos]
    if curPage == 1 and allPage == 1:  # 标记1
        allPostCounts = ShipmentOrder.objects.count()
        allPage = int(allPostCounts / settings.ONE_PAGE_OF_DATA)
        remainPost = allPostCounts % settings.ONE_PAGE_OF_DATA
        if remainPost > 0:
            allPage += 1
    return render(request, "finance/add/receivable-list.html", {'order': order_list,
                                                                'allPage': allPage,
                                                                'curPage': curPage
                                                                })


# 添加付款单
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def make_payment(request, order_id):
    request.session.set_expiry(request.session.get_expiry_age())
    role = utils.get_user_type(request)
    if role != 0 and role != 4:
        return render(request, 'error/permission.html')

    order = get_object_or_404(ShipmentOrder, pk=order_id)
    order.payable = order.totalPrice - order.paid_price
    if request.method == "POST":
        form = PaymentOrderCreationForm(request.POST)
        if form.is_valid():
            # update order
            if form.cleaned_data["amount"] > order.payable:
                return HttpResponse("错误：支付金额不得大于应收款项，请返回重试。")
            form.save(shipment_order=order, handle=request.user)
            order.paid_price = Decimal(order.paid_price) + Decimal(form.cleaned_data["amount"])
            order.payable = Decimal(order.totalPrice) - Decimal(order.paid_price)
            order.save()
            return receivable_list(request)
    else:
        form = PaymentOrderCreationForm()
    return render(request, "finance/add/form-makepayment.html", {'order': order,
                                                                 'form': form})


# 管理付款单
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def manage_payment_record(request):
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
    order_list = PaymentOrder.objects.all().order_by("-payment_date")[startPos:endPos]
    if curPage == 1 and allPage == 1:  # 标记1
        allPostCounts = PaymentOrder.objects.count()
        allPage = int(allPostCounts / settings.ONE_PAGE_OF_DATA)
        remainPost = allPostCounts % settings.ONE_PAGE_OF_DATA
        if remainPost > 0:
            allPage += 1
    return render(request, "finance/manage/payment-record-manager.html", {'order': order_list,
                                                                          'allPage': allPage,
                                                                          'curPage': curPage
                                                                          })


# 付款单详情
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def payment_record_detail(request, order_id):
    request.session.set_expiry(request.session.get_expiry_age())
    order = get_object_or_404(PaymentOrder, pk=order_id)
    return render(request, 'finance/manage/payment-record-detail.html', {'order': order})


# 付款单修改
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def payment_record_modify(request, order_id):
    request.session.set_expiry(request.session.get_expiry_age())
    role = utils.get_user_type(request)
    if role != 0 and role != 4:
        return render(request, 'error/permission.html')
    request.session['order_manage'] = order_id
    order_instance = get_object_or_404(PaymentOrder, id=order_id)
    order_form = PaymentOrderCreationForm(request.POST or None, instance=order_instance)

    if order_form.is_valid():
        order_form.save(shipment_order=order_instance.shipment_order, handle=request.user)
        return render(request, "finance/manage/payment-order-modify-complete.html")
    return render(request, "finance/manage/payment-record-modify.html", {'form': order_form,
                                                                         'order': order_id})



# 管理付款单 付款单搜索
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def payment_order_search(request):
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
    all_payment_order = PaymentOrder.objects.filter(
        Q(shipment_order__comments__icontains=query) |
        Q(shipment_order__receiver__icontains=query) |
        Q(shipment_order__sender__icontains=query) |
        Q(shipment_order__from_address__icontains=query) |
        Q(shipment_order__to_address__icontains=query) |
        Q(shipment_order__market__icontains=query) |
        Q(shipment_order__handle__username__icontains=query) |
        Q(shipment_order__sender_contact__icontains=query) |
        Q(shipment_order__receiver_contact__icontains=query) |
        Q(shipment_order__mode__icontains=query) |
        Q(handle__username__icontains=query) |
        Q(comments__icontains=query)
    ).count()
    payment_order = PaymentOrder.objects.filter(
        Q(shipment_order__comments__icontains=query) |
        Q(shipment_order__receiver__icontains=query) |
        Q(shipment_order__sender__icontains=query) |
        Q(shipment_order__from_address__icontains=query) |
        Q(shipment_order__to_address__icontains=query) |
        Q(shipment_order__market__icontains=query) |
        Q(shipment_order__handle__username__icontains=query) |
        Q(shipment_order__sender_contact__icontains=query) |
        Q(shipment_order__receiver_contact__icontains=query) |
        Q(shipment_order__mode__icontains=query) |
        Q(handle__username__icontains=query) |
        Q(comments__icontains=query)).order_by("-payment_date")[startPos:endPos]
    if curPage == 1 and allPage == 1:  # 标记1
        allPostCounts = all_payment_order
        allPage = int(allPostCounts / settings.ONE_PAGE_OF_DATA)
        remainPost = allPostCounts % settings.ONE_PAGE_OF_DATA
        if remainPost > 0:
            allPage += 1
    return render(request, "finance/manage/payment-record-manager.html", {'order': payment_order,
                                                                          'allPage': allPage,
                                                                          'curPage': curPage})


# 管理付款单 高级搜索
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def payment_order_search_advanced(request):
    request.session.set_expiry(request.session.get_expiry_age())
    return render(request, "finance/search/payment-order-search.html")


# 管理付款单 高级搜索 结果
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def payment_order_search_advanced_result(request):
    request.session.set_expiry(request.session.get_expiry_age())
    keyword = request.GET.get('keyword')
    start_date = request.GET.get('start_date', "")
    end_date = request.GET.get('end_date')
    payment_amount = request.GET.get('payment_amount')
    if payment_amount is "":
        payment_amount = 0
    else:
        payment_amount = float(payment_amount)
    if start_date is "": start_date = "1970-1-1"
    if end_date is "": end_date = datetime.datetime.now().strftime("%Y-%m-%d")

    result = PaymentOrder.objects.filter(
        Q(shipment_order__comments__icontains=keyword) |
        Q(shipment_order__receiver__icontains=keyword) |
        Q(shipment_order__sender__icontains=keyword) |
        Q(shipment_order__from_address__icontains=keyword) |
        Q(shipment_order__to_address__icontains=keyword) |
        Q(shipment_order__market__icontains=keyword) |
        Q(shipment_order__handle__username__icontains=keyword) |
        Q(shipment_order__sender_contact__icontains=keyword) |
        Q(shipment_order__receiver_contact__icontains=keyword) |
        Q(shipment_order__mode__icontains=keyword) |
        Q(handle__username__icontains=keyword) |
        Q(comments__icontains=keyword),
        Q(payment_date__range=(start_date, end_date)),
        Q(amount__gte=payment_amount)
    ).order_by("-payment_date")
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
    return render(request, "finance/search/payment-order-search-result.html", {"order": order,
                                                                               "keyword": keyword,
                                                                               "payment_amount": payment_amount,
                                                                               'start_date': start_date,
                                                                               'end_date': end_date,
                                                                               'allPage': allPage,
                                                                               'curPage': curPage
                                                                               })

