from django.db import models
from users.models import User


class Ad(models.Model):
    title = models.CharField(max_length=60)
    price = models.PositiveIntegerField(default=0)
    description = models.TextField(max_length=300, default='', null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default='', related_name='ads')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='ad_images/', null=True)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-created_at']
