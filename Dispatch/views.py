from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from Dispatch.forms import DriverCreationForm
from Dispatch.models import Driver, DispatchRecord
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


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
    driver = get_object_or_404(Driver, pk=driver_id)
    return render(request, "dispatch/driver/driver-detail.html", {'driver': driver})


# 司机详情
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

