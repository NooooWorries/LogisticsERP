from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required(login_url='/error/not-logged-in/')
def index(request):
    user = request.user
    return render(request, 'index.html', {'user': user})


def error_404(request):
    data = {}
    return render(request, 'error/404.html', data)


def error_500(request):
    data = {}
    return render(request, 'error/500.html', data)


def error_not_logged_in(request):
    data = {}
    return render(request, 'error/not-logged-in.html', data)
