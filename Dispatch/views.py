from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from Dispatch.forms import DriverCreationForm, DispatchRecordCreationForm
from Dispatch.models import Driver, DispatchRecord
from ShipmentOrder.models import Goods
from django.db.models import Q
import barcode
from barcode.writer import ImageWriter
from django.template.loader import get_template
from xhtml2pdf import pisa
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from LogisticsERP import settings, utils
import os
from xhtml2pdf.default import DEFAULT_FONT
import datetime


# 添加司机
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def add_driver(request):
    request.session.set_expiry(request.session.get_expiry_age())
    role = utils.get_user_type(request)
    if role != 0 and role != 3:
        return render(request, 'error/permission.html')
    if request.method == 'POST':
        form = DriverCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return manage_driver(request)
    else:
        form = DriverCreationForm()
    return render(request, 'dispatch/driver/form-add-driver.html', {'form': form})


# 管理司机
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def manage_driver(request):
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
    driver = Driver.objects.all()[startPos:endPos]
    # 计算所负责的订单数量
    for item in driver:
        item.dispatch_count = DispatchRecord.objects.filter(driver_id=item.id).count()
    if curPage == 1 and allPage == 1:  # 标记1
        allPostCounts = Driver.objects.count()
        allPage = int(allPostCounts / settings.ONE_PAGE_OF_DATA)
        remainPost = allPostCounts % settings.ONE_PAGE_OF_DATA
        if remainPost > 0:
            allPage += 1
    return render(request, "dispatch/driver/driver-manager.html", {'driver': driver,
                                                                   'allPage': allPage,
                                                                   'curPage': curPage})


# 司机搜索
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def driver_search(request):
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
    all_driver = Driver.objects.filter(Q(name__icontains=query) |
                                   Q(identity_number__icontains=query) |
                                   Q(license__icontains=query) |
                                   Q(comments__icontains=query)).count()
    driver = Driver.objects.filter(Q(name__icontains=query) |
                                   Q(identity_number__icontains=query) |
                                   Q(license__icontains=query) |
                                   Q(comments__icontains=query))[startPos:endPos]
    # 计算所负责的订单数量
    for item in driver:
        item.dispatch_count = all_driver
    if curPage == 1 and allPage == 1:  # 标记1
        allPostCounts = all_driver
        allPage = int(allPostCounts / settings.ONE_PAGE_OF_DATA)
        remainPost = allPostCounts % settings.ONE_PAGE_OF_DATA
        if remainPost > 0:
            allPage += 1
    return render(request, "dispatch/driver/driver-manager.html", {'driver': driver,
                                                                   'allPage': allPage,
                                                                   'curPage': curPage})


# 司机详情
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def driver_detail(request, driver_id):
    request.session.set_expiry(request.session.get_expiry_age())
    driver_instance = get_object_or_404(Driver, pk=driver_id)
    order = DispatchRecord.objects.filter(driver=driver_id)
    return render(request, "dispatch/driver/driver-detail.html", {'driver': driver_instance,
                                                                  'order': order})


# 编辑司机
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def driver_modify(request, driver_id):
    request.session.set_expiry(request.session.get_expiry_age())
    role = utils.get_user_type(request)
    if role != 0 and role != 3:
        return render(request, 'error/permission.html')
    driver_instance = get_object_or_404(Driver, pk=driver_id)
    driver_form = DriverCreationForm(request.POST or None, instance=driver_instance)
    if driver_form.is_valid():
        driver_form.save()
        return render(request, "dispatch/driver/customer-class-modify-complete.html")
    return render(request, "dispatch/driver/driver-modify.html", {'form': driver_form})


# 创建出车订单
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def add_dispatch_order(request):
    request.session.set_expiry(request.session.get_expiry_age())
    role = utils.get_user_type(request)
    if role != 0 and role != 3:
        return render(request, 'error/permission.html')
    if request.method == 'POST':
        form = DispatchRecordCreationForm(request.POST)
        if form.is_valid():
            order = form.save()
            return redirect(add_dispatch_order_choose_good, order.id)
    else:
        form = DispatchRecordCreationForm()
    return render(request, 'dispatch/record/add/form-add-dispatch-record.html', {'form': form})


# 创建出车订单 选择货物
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def add_dispatch_order_choose_good(request, order_id):
    request.session.set_expiry(request.session.get_expiry_age())
    role = utils.get_user_type(request)
    if role != 0 and role != 3:
        return render(request, 'error/permission.html')
    order = get_object_or_404(DispatchRecord, pk=order_id)
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
    good_all = Goods.objects.filter(Q(dispatch_id__isnull=True) | Q(dispatch=order_id)).count()
    good = Goods.objects.filter(Q(dispatch_id__isnull=True) | Q(dispatch=order_id))[startPos:endPos]
    if curPage == 1 and allPage == 1:  # 标记1
        allPostCounts = good_all
        allPage = int(allPostCounts / settings.ONE_PAGE_OF_DATA)
        remainPost = allPostCounts % settings.ONE_PAGE_OF_DATA
        if remainPost > 0:
            allPage += 1
    return render(request, 'dispatch/record/add/from-add-dispatch-choose-goods.html', {"order": order,
                                                                                       "good": good,
                                                                                       'allPage': allPage,
                                                                                       'curPage': curPage})


# 选择货物 ajax
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def ajax_select_good(request, order_id, good_id):
    request.session.set_expiry(request.session.get_expiry_age())
    role = utils.get_user_type(request)
    if role != 0 and role != 3:
        return render(request, 'error/permission.html')
    good = get_object_or_404(Goods, pk=good_id)
    order = get_object_or_404(DispatchRecord, pk=order_id)
    good.dispatch = order
    good.save()
    return HttpResponse('{"status": "success"}', content_type="application/json")


# 取消选择货物 ajax
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def ajax_select_good_cancel(request, good_id):
    request.session.set_expiry(request.session.get_expiry_age())
    role = utils.get_user_type(request)
    if role != 0 and role != 3:
        return render(request, 'error/permission.html')
    good = get_object_or_404(Goods, pk=good_id)
    good.dispatch = None
    good.save()
    return HttpResponse('{"status": "success"}', content_type="application/json")


# 货物订单 明细确认
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def add_dispatch_order_summary(request, order_id):
    request.session.set_expiry(request.session.get_expiry_age())
    role = utils.get_user_type(request)
    if role != 0 and role != 3:
        return render(request, 'error/permission.html')
    order = get_object_or_404(DispatchRecord, pk=order_id)
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
    good_all = Goods.objects.filter(dispatch=order_id).count()
    good = Goods.objects.filter(dispatch=order_id)[startPos:endPos]
    if curPage == 1 and allPage == 1:  # 标记1
        allPostCounts = good_all
        allPage = int(allPostCounts / settings.ONE_PAGE_OF_DATA)
        remainPost = allPostCounts % settings.ONE_PAGE_OF_DATA
        if remainPost > 0:
            allPage += 1
    return render(request, 'dispatch/record/add/from-add-dispatch-summary.html', {"order": order,
                                                                                  "good": good,
                                                                                  'allPage': allPage,
                                                                                  'curPage': curPage})


# 生成出车单pdf
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def generate_PDF(request, order_id):
    request.session.set_expiry(request.session.get_expiry_age())
    role = utils.get_user_type(request)
    if role != 0 and role != 3:
        return render(request, 'error/permission.html')
    order = get_object_or_404(DispatchRecord, pk=order_id)
    order.status = 1
    order.save()
    good = Goods.objects.filter(dispatch=order_id)
    for item in good:
        good_ean = barcode.get("Code39", str(item.id), writer=ImageWriter())
        good_ean.default_writer_options['write_text'] = False
        good_barcode = good_ean.save("OrderPDF/barcode/gd_" + str(item.id))
        item.barcode = good_barcode
    ean = barcode.get("Code39", str(order_id), writer=ImageWriter())
    ean.default_writer_options['write_text'] = False
    barcode_img = ean.save("OrderPDF/barcode/" + str(order_id))
    data = {'order': order, 'good': good, 'today': datetime.datetime.now().strftime("%Y-%m-%d"), 'barcode': barcode_img}
    html = get_template('dispatch/pdf.html').render(data)
    file = open("OrderPDF/documents/" + str(order_id) + ".pdf", "w+b")
    pdfmetrics.registerFont(TTFont("yh", os.path.join(settings.DOMAIN_NAME, 'static/fonts/fzlt.ttf')))
    DEFAULT_FONT['helvetica'] = 'yh'
    pisa.CreatePDF(html.encode('utf-8'), dest=file, encoding='utf-8', )
    file.seek(0)
    pdf = file.read()
    file.close()
    return HttpResponse(pdf, 'application/pdf')


# 删除司机
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def driver_delete(request, driver_id):
    request.session.set_expiry(request.session.get_expiry_age())
    role = utils.get_user_type(request)
    if role != 0 and role != 3:
        return render(request, 'error/permission.html')
    driver = get_object_or_404(Driver, pk=driver_id)
    dispatch_count = DispatchRecord.objects.filter(driver_id=driver.id).count()
    if dispatch_count <= 0:
        driver.delete()
    return redirect(manage_driver)


# 管理出车单
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def manage_dispatch_order(request):
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
    order = DispatchRecord.objects.all()[startPos:endPos]
    if curPage == 1 and allPage == 1:  # 标记1
        allPostCounts = DispatchRecord.objects.count()
        allPage = int(allPostCounts / settings.ONE_PAGE_OF_DATA)
        remainPost = allPostCounts % settings.ONE_PAGE_OF_DATA
        if remainPost > 0:
            allPage += 1
    return render(request, "dispatch/record/manage/dispatch-order-manager.html", {'order': order,
                                                                                  'allPage': allPage,
                                                                                  'curPage': curPage})


# 出车单搜索
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def dispatch_order_search(request):
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
    all_order = DispatchRecord.objects.filter(Q(driver__name__icontains=query) |
                                          Q(vehicle_number__icontains=query) |
                                          Q(origin__icontains=query) |
                                          Q(destination__icontains=query) |
                                          Q(comments__icontains=query)).count()
    order = DispatchRecord.objects.filter(Q(driver__name__icontains=query) |
                                          Q(vehicle_number__icontains=query) |
                                          Q(origin__icontains=query) |
                                          Q(destination__icontains=query) |
                                          Q(comments__icontains=query))[startPos:endPos]
    if curPage == 1 and allPage == 1:  # 标记1
        allPostCounts = all_order
        allPage = int(allPostCounts / settings.ONE_PAGE_OF_DATA)
        remainPost = allPostCounts % settings.ONE_PAGE_OF_DATA
        if remainPost > 0:
            allPage += 1
    return render(request, "dispatch/record/manage/dispatch-order-manager.html", {'order': order,
                                                                                  'allPage': allPage,
                                                                                  'curPage': curPage})


# 出车单详情
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def dispatch_order_detail(request, order_id):
    request.session.set_expiry(request.session.get_expiry_age())
    order = get_object_or_404(DispatchRecord, pk=order_id)
    good = Goods.objects.filter(dispatch=order_id)
    return render(request, "dispatch/record/manage/dispatch-order-detail.html", {'order': order,
                                                                                 'good': good})


# 删除出车记录
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def dispatch_order_delete(request, order_id):
    request.session.set_expiry(request.session.get_expiry_age())
    role = utils.get_user_type(request)
    if role != 0 and role != 3:
        return render(request, 'error/permission.html')
    order = get_object_or_404(DispatchRecord, pk=order_id)
    if order.status == 0:
        order.delete()
    return redirect(manage_dispatch_order)


# 出车单 草稿箱
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def draft_dispatch_order(request):
    request.session.set_expiry(request.session.get_expiry_age())
    role = utils.get_user_type(request)
    if role != 0 and role != 3:
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
    order_all = DispatchRecord.objects.filter(status__exact=0).count()
    order = DispatchRecord.objects.filter(status__exact=0)[startPos:endPos]
    if curPage == 1 and allPage == 1:  # 标记1
        allPostCounts = order_all
        allPage = int(allPostCounts / settings.ONE_PAGE_OF_DATA)
        remainPost = allPostCounts % settings.ONE_PAGE_OF_DATA
        if remainPost > 0:
            allPage += 1
    return render(request, "dispatch/record/draft/dispatch-order-draft.html", {'order': order,
                                                                               'allPage': allPage,
                                                                               'curPage': curPage})


# 出车单 修改
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def dispatch_order_modify(request, order_id):
    request.session.set_expiry(request.session.get_expiry_age())
    role = utils.get_user_type(request)
    if role != 0 and role != 3:
        return render(request, 'error/permission.html')
    order_instance = get_object_or_404(DispatchRecord, pk=order_id)
    form = DispatchRecordCreationForm(request.POST or None, instance=order_instance)
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
    good_all = Goods.objects.filter(Q(dispatch_id__isnull=True) | Q(dispatch=order_id)).count()
    good = Goods.objects.filter(Q(dispatch_id__isnull=True) | Q(dispatch=order_id))[startPos:endPos]
    if curPage == 1 and allPage == 1:  # 标记1
        allPostCounts = good_all
        allPage = int(allPostCounts / settings.ONE_PAGE_OF_DATA)
        remainPost = allPostCounts % settings.ONE_PAGE_OF_DATA
        if remainPost > 0:
            allPage += 1
    if form.is_valid():
        form.save()
        return render(request, 'dispatch/record/manage/dispatch-order-modify-complete.html')
    return render(request, 'dispatch/record/manage/dispatch-order-modify.html', {'form': form,
                                                                                 "order": order_instance,
                                                                                 "good": good,
                                                                                 'allPage': allPage,
                                                                                 'curPage': curPage})


# 管理出车单 出车单高级搜索
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def dispatch_order_search_advanced(request):
    request.session.set_expiry(request.session.get_expiry_age())
    return render(request, "dispatch/record/search/dispatch-order-search.html")


# 管理出车单 订单高级搜索结果
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def dispatch_order_search_advanced_result(request):
    request.session.set_expiry(request.session.get_expiry_age())
    keyword = request.GET.get('keyword')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    status = request.GET.get('status')
    if start_date is "": start_date = "1970-1-1"
    if end_date is "": end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    if status is not "":
        status = int(request.GET.get('status'))
        result = DispatchRecord.objects.filter(
            Q(driver__name__icontains=keyword) |
            Q(vehicle_number__icontains=keyword) |
            Q(origin__icontains=keyword) |
            Q(destination__icontains=keyword) |
            Q(comments__icontains=keyword),
            Q(dispatch_date__range=(start_date, end_date)),
            Q(status__exact=status)
        )
        result_count = result.count()
    else:
        result = DispatchRecord.objects.filter(
            Q(driver__name__icontains=keyword) |
            Q(vehicle_number__icontains=keyword) |
            Q(origin__icontains=keyword) |
            Q(destination__icontains=keyword) |
            Q(comments__icontains=keyword),
            Q(dispatch_date__range=(start_date, end_date))
        )
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
    return render(request, "dispatch/record/search/dispatch-order-search-result.html", {'order': order,
                                                                          'keyword': keyword,
                                                                          'start_date': start_date,
                                                                          'end_date': end_date,
                                                                          'status': status,
                                                                          'allPage': allPage,
                                                                          'curPage': curPage})


# 出车单 送达确认
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def arrival_dispatch_order(request):
    request.session.set_expiry(request.session.get_expiry_age())
    role = utils.get_user_type(request)
    if role != 0 and role != 3:
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
    order_all = DispatchRecord.objects.filter(Q(status__exact=1) and Q(driver__account__exact=request.user)).count()
    order = DispatchRecord.objects.filter(Q(status__exact=1) and Q(driver__account__exact=request.user))[startPos:endPos]
    if curPage == 1 and allPage == 1:  # 标记1
        allPostCounts = order_all
        allPage = int(allPostCounts / settings.ONE_PAGE_OF_DATA)
        remainPost = allPostCounts % settings.ONE_PAGE_OF_DATA
        if remainPost > 0:
            allPage += 1
    return render(request, "dispatch/record/arrival/dispatch-order-arrival.html", {'order': order,
                                                                                   'allPage': allPage,
                                                                                   'curPage': curPage})


# 出车单 送达 详情
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def arrival_dispatch_order_detail(request, order_id):
    request.session.set_expiry(request.session.get_expiry_age())
    role = utils.get_user_type(request)
    if role != 0 and role != 3:
        return render(request, 'error/permission.html')
    order = get_object_or_404(DispatchRecord, pk=order_id)
    good = Goods.objects.filter(dispatch=order_id)
    return render(request, 'dispatch/record/arrival/dispatch-order-arrival-detail.html', {'order': order,
                                                                                          'good': good})


# 出车单 送达 确认
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def arrival_dispatch_order_confirm(request, order_id):
    request.session.set_expiry(request.session.get_expiry_age())
    role = utils.get_user_type(request)
    if role != 0 and role != 3:
        return render(request, 'error/permission.html')
    # 出车单标记送达
    dispatch_order = get_object_or_404(DispatchRecord, pk=order_id)
    dispatch_order.status = 2
    dispatch_order.save()

    # 出车单下所有货物标记为到达
    dispatch_good = Goods.objects.filter(dispatch=order_id)
    for item in dispatch_good:
        item.status = 2
        item.save()

    # 列出运送订单
    ids = []
    for item in dispatch_good:
        ids.append(item.shipment_order_id)
    ids = list(set(ids))

    # 检查是否到达
    for i in range(len(ids)):
        shipment_order = ids[i]
        is_finished = True
        goods = Goods.objects.filter(shipment_order_id=ids[i])
        for good in goods:
            if good.status is not 2:
                is_finished = False
                break
        if is_finished:
            shipment_order.status = 3
            shipment_order.save()

    return HttpResponse(ids)


