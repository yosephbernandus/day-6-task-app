from functools import wraps
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from typing import Any, Callable

def login_required(view_func: Callable) -> Callable:
    @wraps(view_func)
    def _check_user_account(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        messages.info(request, 'Mohon masuk terelebih dahulu')
        return redirect('authentication:login')
    return _check_user_account
