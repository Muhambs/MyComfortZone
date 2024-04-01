from functools import wraps

from django.urls import reverse

from .models import Profile
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect

from functools import wraps
from django.shortcuts import redirect

def patient_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        if request.user.is_authenticated and request.user.is_patient:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('patientlogin')
    return _wrapped_view

def doctor_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
            if not profile.is_doctor:
                return HttpResponseRedirect(reverse('not_authorized_url'))
        except Profile.DoesNotExist:
            return HttpResponseRedirect(reverse('profile_creation_url'))

        return view_func(request, *args, **kwargs)
    return _wrapped_view
