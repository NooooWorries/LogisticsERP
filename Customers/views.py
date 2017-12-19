from django.http import HttpResponse
from django.shortcuts import render
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
    customer_class = get_object_or_404(CustomerClass, pk=class_id)
    return render(request, "customer/class/customer-class-detail.html", {'customer_class': customer_class})


# 管理客户组 编辑页
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def customer_class_modify(request, class_id):
    request.session['order_manage'] = class_id
    class_instance = get_object_or_404(CustomerClass, id=class_id)
    class_form = CustomerClassCreationForm(request.POST or None, instance=class_instance)

    if class_form.is_valid():
        class_form.save()
        return render(request, "customer/class/customer-class-modify-complete.html")
    return render(request, "customer/class/customer-class-modify.html", {'form': class_form,
                                                                         'customer_class': class_id})


# 添加客户
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def add_customer(request):
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