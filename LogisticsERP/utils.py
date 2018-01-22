from Account.models import UserProfile
from django.shortcuts import get_object_or_404


def get_user_type(request):
    current_user_id = request.user.id
    profile = get_object_or_404(UserProfile, pk=current_user_id)
    request.session["role"] = profile.role
    return profile.role
