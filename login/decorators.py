from django.shortcuts import redirect
from django.contrib import messages

def login_required_custom(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get("user_id"):
            messages.error(request, "You must be logged in to access this page.")
            return redirect("loginapp:login")  # Redirect to your customer login page
        return view_func(request, *args, **kwargs)
    return wrapper