from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from Customers.forms import CustomerClassCreationForm, CustomerCreationForm
from ShipmentOrder.models import CustomerClass, Customer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


# 添加客户组
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def add_customer_class(request):
    request.session.set_expiry(request.session.get_expiry_age())
    if request.method == "POST":
        form = CustomerClassCreationForm(request.POST)
        if form.is_valid():
            customer_class = form.save(commit=False)
            customer_class.save()
            return customer_class(request)
    else:
        form = CustomerClassCreationForm()
    return render(request, "customer/class/form-addcustomerclass.html", {'form': form})


# 查询客户组 所有客户组
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def customer_class(request):
    request.session.set_expiry(request.session.get_expiry_age())
    page = request.GET.get('page')
    customer_class_list = CustomerClass.objects.all()
    paginator = Paginator(customer_class_list, 10)
    try:
        customer_class = paginator.page(page)
    except PageNotAnInteger:
        customer_class = paginator.page(1)
    except EmptyPage:
        customer_class = paginator.page(paginator.num_pages)
    return render(request, "customer/class/customer-class-manager.html", {'customer_class': customer_class})


# 管理客户组 客户组搜索
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def customer_class_search(request):
    request.session.set_expiry(request.session.get_expiry_age())
    query = request.GET.get('query')
    page = request.GET.get('page')
    result = CustomerClass.objects.filter(
        Q(class_name__icontains=query) |
        Q(comments__icontains=query))
    paginator = Paginator(result, 10)
    try:
        customer_class = paginator.page(page)
    except PageNotAnInteger:
        customer_class = paginator.page(1)
    except EmptyPage:
        customer_class = paginator.page(paginator.num_pages)
    return render(request, "customer/class/customer-class-manager.html", {'customer_class': customer_class, 'query': query})


# 管理客户组 详情页
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def customer_class_detail(request, class_id):
    request.session.set_expiry(request.session.get_expiry_age())
    page = request.GET.get('page')
    customer_class = get_object_or_404(CustomerClass, pk=class_id)
    customer_list = Customer.objects.filter(customer_class_id=class_id)
    paginator = Paginator(customer_list, 10)
    try:
        customer = paginator.page(page)
    except PageNotAnInteger:
        customer = paginator.page(1)
    except EmptyPage:
        customer = paginator.page(paginator.num_pages)
    return render(request, "customer/class/customer-class-detail.html", {'customer_class': customer_class,
                                                                         'customer': customer})


# 管理客户组 编辑页
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def customer_class_modify(request, class_id):
    request.session.set_expiry(request.session.get_expiry_age())
    request.session['order_manage'] = class_id
    class_instance = get_object_or_404(CustomerClass, id=class_id)
    class_form = CustomerClassCreationForm(request.POST or None, instance=class_instance)

    if class_form.is_valid():
        class_form.save()
        return render(request, "customer/class/customer-class-modify-complete.html")
    return render(request, "customer/class/customer-class-modify.html", {'form': class_form,
                                                                         'customer_class': class_id})


# 管理客户组 确认删除
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def customer_class_confirm_delete(request, class_id):
    request.session.set_expiry(request.session.get_expiry_age())
    customer_class_instance = get_object_or_404(CustomerClass, pk=class_id)
    customer_count = Customer.objects.filter(customer_class_id=class_id).count()
    return render(request, "customer/class/customer-class-delete-confirm.html", {'customer_class': customer_class_instance,
                                                                          'customer_count': customer_count})


# 管理客户组 客户组
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def customer_class_delete(request, class_id):
    request.session.set_expiry(request.session.get_expiry_age())
    customer_class_object = get_object_or_404(CustomerClass, pk=class_id)
    customer_class_object.delete()
    return render(request, "customer/class/customer-class-delete-complete.html")


# 添加客户
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def add_customer(request):
    request.session.set_expiry(request.session.get_expiry_age())
    if request.method == "POST":
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.save()
            return HttpResponse("success")
    else:
        form = CustomerCreationForm()
    return render(request, "customer/user/form-addcustomer.html", {'form': form})


# 查询客户 所有客户
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def customer(request):
    request.session.set_expiry(request.session.get_expiry_age())
    page = request.GET.get('page')
    customer_list = Customer.objects.all()
    paginator = Paginator(customer_list, 10)
    try:
        customer = paginator.page(page)
    except PageNotAnInteger:
        customer = paginator.page(1)
    except EmptyPage:
        customer = paginator.page(paginator.num_pages)
    return render(request, "customer/user/customer-manager.html", {'customer': customer})


# 管理客户 客户搜索
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def customer_search(request):
    request.session.set_expiry(request.session.get_expiry_age())
    query = request.GET.get('query')
    page = request.GET.get('page')
    result = Customer.objects.filter(
        Q(customer_class__class_name__icontains=query) |
        Q(customer_name__icontains=query) |
        Q(contact_person__icontains=query) |
        Q(contact_number__icontains=query) |
        Q(identity_number__icontains=query) |
        Q(address__icontains=query) |
        Q(comments__icontains=query))
    paginator = Paginator(result, 10)
    try:
        customer = paginator.page(page)
    except PageNotAnInteger:
        customer = paginator.page(1)
    except EmptyPage:
        customer = paginator.page(paginator.num_pages)
    return render(request, "customer/user/customer-manager.html", {'customer': customer, 'query': query})


# 管理客户 编辑页
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def customer_modify(request, customer_id):
    request.session.set_expiry(request.session.get_expiry_age())
    request.session['order_manage'] = customer_id
    customer_instance = get_object_or_404(Customer, id=customer_id)
    customer_form = CustomerCreationForm(request.POST or None, instance=customer_instance)
    if customer_form.is_valid():
        customer_form.save()
        return render(request, "customer/user/customer-modify-complete.html")
    return render(request, "customer/user/customer-modify.html", {'form': customer_form,
                                                                  'customer_class': customer_id})


# 管理客户 详情页
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def customer_detail(request, customer_id):
    request.session.set_expiry(request.session.get_expiry_age())
    customer = get_object_or_404(Customer, pk=customer_id)
    return render(request, "customer/user/customer-detail.html", {'customer': customer})


# 管理客户 确认删除
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def customer_confirm_delete(request, customer_id):
    request.session.set_expiry(request.session.get_expiry_age())
    customer_instance = get_object_or_404(Customer, pk=customer_id)
    return render(request, "customer/user/customer-delete-confirm.html", {'customer': customer_instance})


# 管理客户 订单删除
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def customer_delete(request, customer_id):
    request.session.set_expiry(request.session.get_expiry_age())
    customer_object = get_object_or_404(Customer, pk=customer_id)
    customer_object.delete()
    return render(request, "customer/user/customer-delete-complete.html")



# 管理客户 高级搜索
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def customer_search_advanced(request):
    request.session.set_expiry(request.session.get_expiry_age())
    customer_class = CustomerClass.objects.all()
    return render(request, "customer/user/customer-search.html", {"customer_class": customer_class})


# 管理客户 高级搜索 结果
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def customer_search_advanced_result(request):
    request.session.set_expiry(request.session.get_expiry_age())
    keyword = request.GET.get('keyword')
    customer_class = request.GET.get('customer_class')
    payable = request.GET.get('payable')
    page = request.GET.get('page')
    if payable is "":
        payable = 0
    else:
        payable = float(payable)
    if customer_class is not "":
        customer_class = int(customer_class)
        result = Customer.objects.filter(
            Q(customer_class__class_name__icontains=keyword) |
            Q(customer_name__icontains=keyword) |
            Q(contact_person__icontains=keyword) |
            Q(contact_number__icontains=keyword) |
            Q(identity_number__icontains=keyword) |
            Q(address__icontains=keyword) |
            Q(comments__icontains=keyword),
            Q(customer_class_id__exact=customer_class),
            payable__gte=payable
        )
    else:
        customer_class = "全部"
        result = Customer.objects.filter(
            Q(customer_class__class_name__icontains=keyword) |
            Q(customer_name__icontains=keyword) |
            Q(contact_person__icontains=keyword) |
            Q(contact_number__icontains=keyword) |
            Q(identity_number__icontains=keyword) |
            Q(address__icontains=keyword) |
            Q(comments__icontains=keyword),
            payable__gte=payable
        )
    paginator = Paginator(result, 10)
    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)
    return render(request, "customer/user/customer-search-result.html", {"customer": result,
                                                                         "keyword": keyword,
                                                                         "class": customer_class,
                                                                         "payable": payable})