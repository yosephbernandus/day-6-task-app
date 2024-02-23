from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):
    id = models.AutoField(db_column='post_id', primary_key=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        db_column='user_id',
        related_name='authors',
        on_delete=models.CASCADE
    )
    slug = models.TextField(db_index=True, blank=True, null=True)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'post'

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    id = models.AutoField(db_column='comment_id', primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='users',
        db_column='user_id',
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()

    class Meta:
        db_table = 'comment'

    def __str__(self) -> int:
        return self.id
