from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from ShipmentOrder.models import ShipmentOrder


@login_required(login_url='/error/not-logged-in/')
def index(request):
    request.session.set_expiry(request.session.get_expiry_age())
    user = request.user
    draft_instances = ShipmentOrder.objects.filter(handle=request.user, status=0)
    draft_count = draft_instances.count()
    audit_instances = ShipmentOrder.objects.filter(status=1)
    audit_count = audit_instances.count()
    request.session['draft'] = draft_count
    request.session['audit'] = audit_count
    return render(request, 'index.html', {'user': user})


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
