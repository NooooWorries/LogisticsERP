from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from ShipmentOrder.models import ShipmentOrder
from Customers.models import Customer, CustomerClass
from Dispatch.models import DispatchRecord
from Finance.models import PaymentOrder
from django.db.models import Q
import datetime
from xlwt import *


def xls_to_response(xls, fname):
    response = HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=%s' % fname
    xls.save(response)
    return response


@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def export_order(request):
    request.session.set_expiry(request.session.get_expiry_age())
    return render(request, "export/export-order.html")


@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def export_order_result(request):
    request.session.set_expiry(request.session.get_expiry_age())
    # 过滤器
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    status = request.GET.get('status')
    if start_date is "":
        start_date = "1970-1-1"
    if end_date is "":
        end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    # 查询所有匹配项
    if status is not "":
        status = int(request.GET.get('status'))
        result = ShipmentOrder.objects.filter(
             Q(create_date__range=(start_date, end_date)),
             Q(status__exact=status))
    else:
        result = ShipmentOrder.objects.filter(Q(create_date__range=(start_date, end_date)))
    # 生成excel文件
    workbook = Workbook(encoding="utf-8")
    worksheet = workbook.add_sheet(u"运送订单")
    worksheet.write(0, 0, "ID")
    worksheet.write(0, 1, "发货人")
    worksheet.write(0, 2, "发出地地址")
    worksheet.write(0, 3, "发出地联系电话")
    worksheet.write(0, 4, "收货人")
    worksheet.write(0, 5, "到达地地址")
    worksheet.write(0, 6, "收货人联系电话")
    worksheet.write(0, 7, "声明价值")
    worksheet.write(0, 8, "保价率")
    worksheet.write(0, 9, "保价费")
    worksheet.write(0, 10, "运费")
    worksheet.write(0, 11, "包装费")
    worksheet.write(0, 12, "总价")
    worksheet.write(0, 13, "运输方式")
    worksheet.write(0, 14, "体积")
    worksheet.write(0, 15, "密度")
    worksheet.write(0, 16, "创建时间")
    worksheet.write(0, 17, "市场")
    worksheet.write(0, 18, "状态")
    worksheet.write(0, 19, "经办")
    worksheet.write(0, 20, "备注")
    excel_row = 1
    for item in result:
        if item.status is 0: status = "未提交"
        if item.status is 1: status = "待审核"
        if item.status is 2: status = "审核通过"
        if item.status is 3: status = "已完成"
        worksheet.write(excel_row, 0, item.id)
        worksheet.write(excel_row, 1, item.sender)
        worksheet.write(excel_row, 2, item.from_address)
        worksheet.write(excel_row, 3, item.sender_contact)
        worksheet.write(excel_row, 4, item.receiver)
        worksheet.write(excel_row, 5, item.to_address)
        worksheet.write(excel_row, 6, item.receiver_contact)
        worksheet.write(excel_row, 7, item.claimed_value)
        worksheet.write(excel_row, 8, item.insurance_rate)
        worksheet.write(excel_row, 9, item.insurance_fee)
        worksheet.write(excel_row, 10, item.freight)
        worksheet.write(excel_row, 11, item.packingFee)
        worksheet.write(excel_row, 12, item.totalPrice)
        worksheet.write(excel_row, 13, item.mode)
        worksheet.write(excel_row, 14, item.volume)
        worksheet.write(excel_row, 15, item.density)
        worksheet.write(excel_row, 16, item.create_date)
        worksheet.write(excel_row, 17, item.market)
        worksheet.write(excel_row, 18, status)
        worksheet.write(excel_row, 19, item.handle.username)
        worksheet.write(excel_row, 20, item.comments)
        excel_row += 1
    return xls_to_response(workbook, "shipment_order.xls")


@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def export_customer(request):
    request.session.set_expiry(request.session.get_expiry_age())
    customer_class = CustomerClass.objects.all()
    return render(request, "export/export-customer.html", {"customer_class": customer_class})


@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def export_customer_result(request):
    request.session.set_expiry(request.session.get_expiry_age())
    customer_class = request.GET.get('customer_class', "")
    # 查询所有匹配项
    if customer_class is not "":
        customer_class = int(customer_class)
        result = Customer.objects.filter(Q(customer_class_id__exact=customer_class))
    else:
        result = Customer.objects.all()
    # 生成excel
    workbook = Workbook(encoding="utf-8")
    worksheet = workbook.add_sheet(u"客户信息")
    worksheet.write(0, 0, "ID")
    worksheet.write(0, 1, "客户名")
    worksheet.write(0, 2, "客户类别")
    worksheet.write(0, 3, "联系人")
    worksheet.write(0, 4, "联系电话")
    worksheet.write(0, 5, "身份证号码")
    worksheet.write(0, 6, "地址")
    worksheet.write(0, 7, "欠款")
    worksheet.write(0, 8, "备注")
    excel_row = 1
    for item in result:
        worksheet.write(excel_row, 0, item.id)
        worksheet.write(excel_row, 1, item.customer_name)
        worksheet.write(excel_row, 2, item.customer_class.class_name)
        worksheet.write(excel_row, 3, item.contact_person)
        worksheet.write(excel_row, 4, item.contact_number)
        worksheet.write(excel_row, 5, item.identity_number)
        worksheet.write(excel_row, 6, item.address)
        worksheet.write(excel_row, 7, item.payable)
        worksheet.write(excel_row, 8, item.comments)
        excel_row += 1
    return xls_to_response(workbook, "customer.xls")


@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def export_dispatch_order(request):
    request.session.set_expiry(request.session.get_expiry_age())
    return render(request, "export/export-dispatch-order.html")


@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def export_dispatch_order_result(request):
    request.session.set_expiry(request.session.get_expiry_age())
    # 过滤器
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    status = request.GET.get('status')
    if start_date is "": start_date = "1970-1-1"
    if end_date is "": end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    # 查询所有匹配项
    if status is not "":
        status = int(request.GET.get('status'))
        result = DispatchRecord.objects.filter(
            Q(dispatch_date__range=(start_date, end_date)),
            Q(status__exact=status)
        )
    else:
        result = DispatchRecord.objects.filter(Q(dispatch_date__range=(start_date, end_date)))
    # 生成excel文件
    workbook = Workbook(encoding="utf-8")
    worksheet = workbook.add_sheet(u"出车记录")
    worksheet.write(0, 0, "ID")
    worksheet.write(0, 1, "司机")
    worksheet.write(0, 2, "车牌号")
    worksheet.write(0, 3, "发车日期")
    worksheet.write(0, 4, "发出地")
    worksheet.write(0, 5, "到达地")
    worksheet.write(0, 6, "备注")
    worksheet.write(0, 7, "状态")
    excel_row = 1
    for item in result:
        if item.status is 0: status = "未提交"
        if item.status is 1: status = "已出车"
        if item.status is 2: status = "已完成"
        worksheet.write(excel_row, 0, item.id)
        worksheet.write(excel_row, 1, item.driver.name)
        worksheet.write(excel_row, 2, item.vehicle_number)
        worksheet.write(excel_row, 3, item.dispatch_date)
        worksheet.write(excel_row, 4, item.origin)
        worksheet.write(excel_row, 5, item.destination)
        worksheet.write(excel_row, 6, item.comments)
        worksheet.write(excel_row, 7, status)
        excel_row += 1
    return xls_to_response(workbook, "dispatch_record.xls")


@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def export_payment_order(request):
    request.session.set_expiry(request.session.get_expiry_age())
    return render(request, "export/export-payment-order.html")


@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def export_payment_order_result(request):
    request.session.set_expiry(request.session.get_expiry_age())
    # 过滤器
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date is "": start_date = "1970-1-1"
    if end_date is "": end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    # 查询所有匹配项
    result = PaymentOrder.objects.filter(Q(payment_date__range=(start_date, end_date)))
    # 生成excel文件
    workbook = Workbook(encoding="utf-8")
    worksheet = workbook.add_sheet(u"收款记录")
    worksheet.write(0, 0, "收款记录ID")
    worksheet.write(0, 1, "付款日期")
    worksheet.write(0, 2, "付款金额")
    worksheet.write(0, 3, "经办")
    worksheet.write(0, 4, "备注")
    worksheet.write(0, 5, "订单ID")
    worksheet.write(0, 6, "发货人")
    worksheet.write(0, 7, "发出地址")
    worksheet.write(0, 8, "发货人联系方式")
    worksheet.write(0, 9, "收货人")
    worksheet.write(0, 10, "收货地址")
    worksheet.write(0, 11, "收货人联系方式")
    worksheet.write(0, 12, "总价")
    excel_row = 1
    for item in result:
        worksheet.write(excel_row, 0, item.id)
        worksheet.write(excel_row, 1, item.payment_date)
        worksheet.write(excel_row, 2, item.amount)
        worksheet.write(excel_row, 3, item.handle.username)
        worksheet.write(excel_row, 4, item.comments)
        worksheet.write(excel_row, 5, item.shipment_order.id)
        worksheet.write(excel_row, 6, item.shipment_order.sender)
        worksheet.write(excel_row, 7, item.shipment_order.from_address)
        worksheet.write(excel_row, 8, item.shipment_order.sender_contact)
        worksheet.write(excel_row, 9, item.shipment_order.receiver)
        worksheet.write(excel_row, 10, item.shipment_order.to_address)
        worksheet.write(excel_row, 11, item.shipment_order.receiver_contact)
        worksheet.write(excel_row, 12, item.shipment_order.totalPrice)
        excel_row += 1
    return xls_to_response(workbook, "payment_record.xls")
