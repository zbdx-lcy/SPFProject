from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class users(AbstractUser):
    phone_number = models.CharField(max_length=15)
    # 添加 related_name 参数以解决冲突
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    def __str__(self):
        return self.username
