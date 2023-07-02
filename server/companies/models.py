from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.db import models


class Company(models.Model):
    '''Класс компании'''

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'
        ordering = ['-updated_at']

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    name = models.CharField(max_length=255, verbose_name='Название компании')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    contact_number = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Почта')
    website = models.URLField(blank=True, verbose_name='Сайт')
    description = models.TextField(blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if self.user.userrole.role != 'employer':
            raise PermissionDenied("Только работадатели 'employer' могут добавить компанию.")
        super().save(*args, **kwargs)


class Contact(models.Model):
    '''Контактное лицо компании'''

    class Meta:
        verbose_name = 'Контактное лицо'
        verbose_name_plural = 'Контактные лица'

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='contacts', verbose_name='Компания')
    name = models.CharField(max_length=255, verbose_name='Имя контакта')
    position = models.CharField(max_length=255, verbose_name='Должность')
    email = models.EmailField(verbose_name='Почта')
    phone_number = models.CharField(max_length=20, verbose_name='Телефон')

    def __str__(self):
        return f'{self.name}'


class Job(models.Model):
    '''Класс вакансии'''

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs', verbose_name='Компания')
    title = models.CharField(max_length=255, verbose_name='Название вакансии')
    description = models.TextField(verbose_name='Описание')
    requirements = models.TextField(verbose_name='Требования')
    conditions = models.TextField(verbose_name='Условия')
    is_open = models.BooleanField(default=True, verbose_name='Открыта')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return f'{self.title} - {self.company.name}'

    def close_job(self):
        self.is_open = False
        self.save()
