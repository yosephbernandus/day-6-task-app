from blog.forms import BlogForm

from django.contrib.auth.models import User
from django.db import connection
from django.http import HttpRequest, HttpResponse 
from django.shortcuts import render

from authentication.decorators import login_required


@login_required
def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'blog/index.html')


@login_required
def submit_post(request: HttpRequest) -> HttpResponse:
    form = BlogForm(data=request.POST or None, user=request.user)

    if form.is_valid():
        form.save()
        return HttpResponse('<p class="success">Form submitted successfully! ✅</p>')

    else:
        return HttpResponse(f'<p class="error">Your form submission was unsuccessful ❌. Please would you correct the errors? The current errors: {form.errors}</p>')


def detail_post(request: HttpRequest, slug: str) -> HttpResponse:

    rows = {}
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT post_id, title, text, created_date from post where slug = %s", [
                slug
            ]
        )
        rows = cursor.fetchone()

    post_data = {
        'id': rows[0],
        'title': rows[1],
        'text': rows[2],
        'created_date': rows[3]
    }
    return  render(request, 'blog/detail_post.html', {'post_data': post_data})
