from django.db import connection
from django import forms
from django.utils import timezone


class BlogForm(forms.Form):
    title = forms.CharField()
    text = forms.CharField()

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def save(self, *args, **kwargs):
        title = self.cleaned_data['title']
        text = self.cleaned_data['text']
        created_date = timezone.localtime()

        rows = None
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO post (title, text, user_id, created_date) VALUES (%s, %s, %s, %s)", [
                    title, text, self.user.id, created_date
                ]
            )
            rows = cursor.fetchone()

        return rows
