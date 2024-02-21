from django.http import HttpRequest, HttpResponse
from django.contrib.auth import login
from django.contrib.admin.forms import AdminAuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages


# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    auth_form = AdminAuthenticationForm(data=request.POST or None)

    if request.POST:
        if auth_form.is_valid():
            login(request, auth_form.get_user())
            return redirect('blog:index')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'auth/index.html')
