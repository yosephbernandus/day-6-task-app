from django.http import HttpRequest, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages


# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'auth/index.html')


def submit_login(request: HttpRequest) -> HttpResponse:
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('landing:blogs')
    else:
        messages.error(request, 'Invalid username or password')
        return render(request, 'auth/index.html')

def logout_view(request):
    logout(request)
    return redirect('landing:index')
