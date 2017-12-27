from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from Dispatch.forms import DriverCreationForm, DispatchRecordCreationForm
from Dispatch.models import Driver, DispatchRecord
from ShipmentOrder.models import Goods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
import barcode
from barcode.writer import ImageWriter
from django.template.loader import get_template
from xhtml2pdf import pisa
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from LogisticsERP import settings
import os
from xhtml2pdf.default import DEFAULT_FONT
import datetime

# 添加司机
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def add_driver(request):
    request.session.set_expiry(request.session.get_expiry_age())
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
    page = request.GET.get('page')
    driver_list = Driver.objects.all()
    for item in driver_list:
        item.dispatch_count = DispatchRecord.objects.filter(driver_id=item.id).count()
    paginator = Paginator(driver_list, 10)
    try:
        driver = paginator.page(page)
    except PageNotAnInteger:
        driver = paginator.page(1)
    except EmptyPage:
       driver = paginator.page(paginator.num_pages)
    return render(request, "dispatch/driver/driver-manager.html", {'driver': driver})


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
    order = get_object_or_404(DispatchRecord, pk=order_id)
    good = Goods.objects.filter(Q(dispatch_id__isnull=True) | Q(dispatch=order_id))
    page = request.GET.get('page')
    paginator = Paginator(good, 10)
    try:
        good = paginator.page(page)
    except PageNotAnInteger:
        good = paginator.page(1)
    except EmptyPage:
        good = paginator.page(paginator.num_pages)
    return render(request, 'dispatch/record/add/from-add-dispatch-choose-goods.html', {"order": order,
                                                                                       "good": good})


# 选择货物 ajax
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def ajax_select_good(request, order_id, good_id):
    request.session.set_expiry(request.session.get_expiry_age())
    good = get_object_or_404(Goods, pk=good_id)
    order = get_object_or_404(DispatchRecord, pk=order_id)
    good.dispatch = order
    good.save()
    return HttpResponse('{"status": "success"}', content_type="application/json")


# 货物订单 明细确认
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def add_dispatch_order_summary(request, order_id):
    request.session.set_expiry(request.session.get_expiry_age())
    page = request.GET.get('page')
    order = get_object_or_404(DispatchRecord, pk=order_id)
    good = Goods.objects.filter(dispatch=order_id)
    paginator = Paginator(good, 10)
    try:
        good = paginator.page(page)
    except PageNotAnInteger:
        good = paginator.page(1)
    except EmptyPage:
        good = paginator.page(paginator.num_pages)
    return render(request, 'dispatch/record/add/from-add-dispatch-summary.html', {"order": order,
                                                                                  "good": good})


# 生成出车单pdf
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def generate_PDF(request, order_id):
    request.session.set_expiry(request.session.get_expiry_age())
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
    page = request.GET.get('page')
    order_list = DispatchRecord.objects.all()
    for item in order_list:
        item.dispatch_count = DispatchRecord.objects.filter(driver_id=item.id).count()
    paginator = Paginator(order_list, 10)
    try:
        order = paginator.page(page)
    except PageNotAnInteger:
        order = paginator.page(1)
    except EmptyPage:
        order = paginator.page(paginator.num_pages)
    return render(request, "dispatch/record/manage/dispatch-order-manager.html", {'order': order})


# 出车单详情
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def dispatch_order_detail(request, order_id):
    request.session.set_expiry(request.session.get_expiry_age())
    order = get_object_or_404(DispatchRecord, pk=order_id)
    good = Goods.objects.filter(dispatch=order_id)
    return render(request, "dispatch/record/manage/dispatch-order-detail.html", {'order': order,
                                                                                 'good': good})