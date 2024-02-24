from django import forms
from django.db import connection
from django.utils import timezone

from django.contrib.auth.models import User
from blog.models import Comment

from typing import Any, Optional


class BlogForm(forms.Form):
    title = forms.CharField()
    text = forms.CharField()

    def __init__(self, user: User, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.user = user

    def save(self) -> Optional[str]:
        title = self.cleaned_data['title']
        text = self.cleaned_data['text']
        created_date = timezone.localtime()

        slug = title.lower().replace(' ', '-')

        post_id = None
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO post (title, text, user_id, created_date) VALUES (%s, %s, %s, %s) RETURNING post_id", [
                    title, text, self.user.id, created_date
                ]
            )
            post_id = cursor.fetchone()[0]
            slug = title.lower().replace(' ', '-')
            transform_slug = f'{slug}-{self.user.id}-{post_id}'
            cursor.execute("UPDATE post SET slug = %s where post_id = %s", [transform_slug, post_id])\

        return post_id


class CommentForm(forms.ModelForm):

    # def __init__(self, user: User, post_id: int, *args: Any, **kwargs: Any) -> None:
    #     super().__init__(*args, **kwargs)
    #     self.user = user
    #     self.post = Post.objects.get(id=post_id)

    class Meta:
        model = Comment
        fields = ['post', 'user', 'text']

