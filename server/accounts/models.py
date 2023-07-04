from django.db import models
from django.contrib.auth.models import User


class UserRole(models.Model):
    '''Класс пользователя с добавлением роли'''

    class Meta:
        verbose_name = 'Роль пользователя'
        verbose_name_plural = 'Роли пользователей'

    ROLES = (
        ('employer', 'Работодатель'),
        ('applicant', 'Соискатель'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    role = models.CharField(max_length=50, choices=ROLES, default='applicant', verbose_name='Роль')

    def __str__(self):
        return f'{self.user.username}'
