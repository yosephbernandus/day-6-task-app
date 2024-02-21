from django.db import connection
from django.shortcuts import render


# Create your views here.
def index(request):
    rows = []
    with connection.cursor() as cursor:
        cursor.execute("SELECT post_id, title, text, created_date from post")
        rows = cursor.fetchall()

    posts = []
    for row in rows:
        obj = {
            'id': row[0],
            'title': row[1],
            'text': row[2],
            'created_date': row[3]
        }
        posts.append(obj)

    context = {
        'posts': posts
    }

    return render(request, 'landing/index.html', context=context)
