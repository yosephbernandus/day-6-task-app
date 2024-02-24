from blog.forms import BlogForm, CommentForm

from django.db import connection
from blog.models import Post
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

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

    comments_data = []
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT c.comment_id, au.username, c.text from comment c join auth_user au on au.id = c.user_id where post_id = %s order by comment_id desc", [rows[0]]
        )
        comment_rows = cursor.fetchall()

        for comment in comment_rows:
            comment_mapping = {
                'comment_id': comment[0],
                'username': comment[1],
                'text': comment[2],
            }
            comments_data.append(comment_mapping)

    post_data = {
        'id': rows[0],
        'title': rows[1],
        'text': rows[2],
        'created_date': rows[3],
        'comments': comments_data,
    }
    return  render(request, 'blog/detail_post.html', {'post_data': post_data})


@login_required
def submit_comment(request: HttpRequest, post_id: int) -> JsonResponse:
    data = {
        'text': request.POST['comment'],
        'user': request.user,
        'post': Post.objects.filter(id=post_id).last()
    }
    form = CommentForm(data=data)

    if form.is_valid():
        comment = form.save()

        comments_datas = []
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT c.comment_id, au.username, c.text from comment c join auth_user au on au.id = c.user_id where post_id = %s order by comment_id desc", [post_id]
            )
            comment_rows = cursor.fetchall()

            for comment in comment_rows:
                comment_mapping = {
                    'comment_id': comment[0],
                    'username': comment[1],
                    'text': comment[2],
                }
                comments_datas.append(comment_mapping)

        comment_html = render_to_string('blog/comment.html', {'comments_datas': comments_datas})
        return JsonResponse({'success': True, 'html': comment_html})

    else:
        errors = form.errors.as_json()
        return JsonResponse({'success': False, 'errors': errors})
