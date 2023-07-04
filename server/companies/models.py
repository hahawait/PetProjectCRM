from slugify import slugify

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied


class Company(models.Model):
    '''Класс компании'''

    class Meta:
        '''Сортировка по дате обновления'''
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'
        ordering = ['-updated_at']

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    name = models.CharField('Название компании', max_length=255)
    slug = models.SlugField('URL', null=False, unique=True, default='')
    address = models.CharField('Адрес', max_length=255)
    contact_number = models.CharField('Телефон', max_length=20)
    email = models.EmailField('Почта')
    website = models.URLField('Сайт', blank=True)
    description = models.TextField('Описание', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

        if self.user.userrole.role != 'employer':
            raise PermissionDenied("Только работадатели 'employer' могут добавить компанию.")
        super().save(*args, **kwargs)


class Contact(models.Model):
    '''Контактное лицо компании'''

    class Meta:
        verbose_name = 'Контактное лицо'
        verbose_name_plural = 'Контактные лица'

    company = models.ForeignKey(Company, on_delete=models.CASCADE,
                                related_name='contacts', verbose_name='Компания')
    name = models.CharField('Имя контакта', max_length=255)
    slug = models.SlugField('URL', null=False)
    position = models.CharField('Должность', max_length=255)
    email = models.EmailField('Почта')
    phone_number = models.CharField('Телефон', max_length=20)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        '''Получает ссылку на контактное лицо по слагу'''
        return reverse("contact-detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Job(models.Model):
    '''Класс вакансии'''

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'

    company = models.ForeignKey(Company, on_delete=models.CASCADE,
                                related_name='jobs', verbose_name='Компания')
    title = models.CharField('Название вакансии', max_length=255)
    slug = models.SlugField('URL', null=True, default='')
    description = models.TextField('Описание')
    requirements = models.TextField('Требования')
    conditions = models.TextField('Условия')
    is_open = models.BooleanField('Статус', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    def __str__(self):
        return f'{self.title} - {self.company.name}'

    def close_job(self):
        '''Закрытие вакансии'''
        self.is_open = False
        self.save()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

