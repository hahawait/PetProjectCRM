from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User

from accounts.models import UserRole
from companies.models import Company
from companies.forms import CompanyForm


class BaseTestCase(TestCase):
    '''Базовый класс теста'''

    def setUp(self):
        '''Тестовые данные'''
        self.client = Client()
        self.user = User.objects.create_user(username='user', password='pass')
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')

        self.user_role = UserRole.objects.create(user=self.user, role='applicant')
        self.user_role1 = UserRole.objects.create(user=self.user1, role='employer')
        self.user_role2 = UserRole.objects.create(user=self.user2, role='employer')

        self.company1 = Company.objects.create(user=self.user1, name='CompanyName1',
                                                contact_number='44-44-44', email='comp1@mail.ru')
        self.company2 = Company.objects.create(user=self.user2, name='CompanyName2',
                                                contact_number='33-33-33', email='comp2@mail.ru')


class CompanyListTest(BaseTestCase):
    '''Тесты для списка компаний'''

    def setUp(self):
        super().setUp()
        self.url = reverse('company-list')


    def test_get_company_list(self):
        '''Получение списка компаний'''

        response = self.client.get(self.url)
        context = response.context

        # Количество компаний в контексте
        company_list = context['company_list']
        self.assertEqual(2, len(company_list))
        # Шаблон
        self.assertTemplateUsed(response, 'companies/company_list.html')
        # Статус код
        self.assertEqual(response.status_code, 200)


    def test_get_company_list_with_query(self):
        '''Получение списка компаний с фильтрацией'''

        response = self.client.get(self.url + '?q=2')
        context = response.context

        # Количество компаний в контексте
        company_list = context['company_list']
        self.assertEqual(1, len(company_list))
        # Шаблон
        self.assertTemplateUsed(response, 'companies/company_list.html')
        # Статус код
        self.assertEqual(response.status_code, 200)


class CompanyDetailTest(BaseTestCase):
    '''Тесты для компании'''

    def setUp(self):
        super().setUp()
        self.url = reverse('company-detail', args=[self.company1.id])


    def test_get_company_detail(self):
        '''Получение компании по id'''

        response = self.client.get(self.url)

        # Шаблон
        self.assertTemplateUsed(response, 'companies/company_detail.html')
        # Статус код
        self.assertEqual(response.status_code, 200)


class CompanyCreateTest(BaseTestCase):
    '''Тесты для создания компании'''

    def setUp(self):
        super().setUp()
        self.url = reverse('company-create')


    def test_get_company_create(self):
        '''GET запрос от соискателя и работадателя'''

        self.client.force_login(self.user)
        response = self.client.get(self.url)

        # HttpResponse
        self.assertContains(response, 'Только работадатели могут добавить компанию')
        # Статус код
        self.assertEqual(response.status_code, 200)

        self.user_role.role = 'employer'
        self.user_role.save()
        response = self.client.get(self.url)

        # Шаблон
        self.assertTemplateUsed(response, 'companies/company_create.html')
        # Форма
        self.assertIsInstance(response.context['form'], CompanyForm)
        # Статус код
        self.assertEqual(response.status_code, 200)


    def test_company_create_user_with_company(self):
        '''GET, POST запросы от работадателя, у которого есть компания'''

        expected_response = 'Вы можете добавить только одну компанию'
        self.client.force_login(self.user1)

        response = self.client.post(self.url)
        # HttpResponse
        self.assertContains(response, expected_response)
        # Статус код
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.url)
        # HttpResponse
        self.assertContains(response, expected_response)
        # Статус код
        self.assertEqual(response.status_code, 200)

# TODO: мб добавить тесты для company_update (логика такая же что и в Create, мб нет смысла)
