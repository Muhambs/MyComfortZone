from functools import wraps

from django.http import HttpResponse
from django.shortcuts import redirect

from functools import wraps
from django.shortcuts import redirect

def patient_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_patient:
            return view_func(request, *args, **kwargs)
        else:
            # Redirect to login page or display a message
            return redirect('patient_login')  # Adjust the URL name as needed
    return _wrapped_view

def doctor_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_doctor:
            return view_func(request, *args, **kwargs)
        else:
            # Redirect to login page or display a message
            return redirect('doctor_login')  # Adjust the URL name as needed
    return _wrapped_view
