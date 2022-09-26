from django.db import models
from users.models import User
from ads.models import Ad


class Comment(models.Model):
    text = models.TextField(max_length=300, default='', null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default='', related_name='comments')
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
