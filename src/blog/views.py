from django.shortcuts import render
from blog.forms import BlogForm
from django.contrib.auth.models import User
from django.http import HttpResponse 


# Create your views here.
def index(request):
    return render(request, 'blog/index.html')


def submit_post(request):
    user = User.objects.last()
    form = BlogForm(data=request.POST or None, user=user)

    if form.is_valid():
        form.save()
        return HttpResponse('<p class="success">Form submitted successfully! ✅</p>')

    else:
        return HttpResponse(f'<p class="error">Your form submission was unsuccessful ❌. Please would you correct the errors? The current errors: {form.errors}</p>')
