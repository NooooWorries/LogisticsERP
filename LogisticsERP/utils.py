from Account.models import UserProfile
from django.shortcuts import get_object_or_404


def get_user_type(request):
    current_user_id = request.user.id
    profile = get_object_or_404(UserProfile, pk=current_user_id)
    request.session["role"] = profile.role
    if profile.role == 0:
        role_text = "管理员"
    elif profile.role == 1:
        role_text = "入库员"
    elif profile.role == 2:
        role_text = "文员"
    elif profile.role == 3:
        role_text = "司机"
    elif profile.role == 4:
        role_text = "财务"
    request.session["role_text"] = role_text
    return profile.role
