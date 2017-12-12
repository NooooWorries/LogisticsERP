from django.shortcuts import render, render_to_response


def display_login(request):
    return render_to_response('registration/login.html')