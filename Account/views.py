from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from Account.forms import UserCreationForm, UserProfileCreationForm
from LogisticsERP import settings, utils


def display_login(request):
    return render_to_response('registration/login.html')


# 添加账户
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def add_account(request):
    request.session.set_expiry(request.session.get_expiry_age())
    role = utils.get_user_type(request)
    if role != 0:
        return render(request, 'error/permission.html')
    if request.method == 'POST':
        form_user = UserCreationForm(request.POST)
        form_profile = UserProfileCreationForm(request.POST)
        if (form_user.is_valid() and form_profile.is_valid()):
            user = form_user.save()
            profile = form_profile.save(commit=False)
            profile.user = user
            profile.id = user.id
            profile.save()
            return render(request, 'system/form-add-user-complete.html')
    else:
        form_user = UserCreationForm()
        form_profile = UserProfileCreationForm()
    return render(request, 'system/form-add-user.html', {'form_user': form_user,
                                                         'form_profile': form_profile})

