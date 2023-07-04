from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User

from accounts.models import UserRole
from companies.models import Company, Contact
from companies.forms import ContactForm


class BaseTestCase(TestCase):
    '''Базовый класс теста'''

    def setUp(self):
        '''Тестовые данные'''
        self.client = Client()

        self.user = User.objects.create_user(username='user', password='pass')
        self.user_with_company = User.objects.create_user(username='user_company', password='pass')

        self.user_role1 = UserRole.objects.create(user=self.user, role='applicant')
        self.user_role2 = UserRole.objects.create(user=self.user_with_company, role='employer')

        self.company = Company.objects.create(user=self.user_with_company, name='CompanyName1',
                                                contact_number='44-44-44', email='comp1@mail.ru')

        self.contact1 = Contact.objects.create(name='Contact1', email='contact1@mail.ru',
                                                company=self.company, position='HR')
        self.contact2 = Contact.objects.create(name='Contact2', email='contact2@mail.ru',
                                                company=self.company, position='Manager')


class ContactListTest(BaseTestCase):
    '''Тесты для списка контактных лиц компании'''

    def setUp(self):
        super().setUp()
        self.url = reverse('contact-list', args=[self.company.id])


    def test_get_contact_list(self):
        '''Получение списка контактных лиц компании'''

        response = self.client.get(self.url)
        context = response.context

        # Количество контактов в контексте
        contact_list = context['contact_list']
        self.assertEqual(2, len(contact_list))
        # Шаблон
        self.assertTemplateUsed(response, 'companies/contact_list.html')
        # Статус код
        self.assertEqual(200, response.status_code)


class ContactDetailTest(BaseTestCase):
    '''Тесты для контактного лица компании'''

    def setUp(self):
        super().setUp()
        self.url = reverse('contact-detail', args=[self.company.id, self.contact1.slug])


    def test_get_contact_detail(self):
        '''Получение контактного лица компании по id'''
        response = self.client.get(self.url)

        # Шаблон
        self.assertTemplateUsed(response, 'companies/contact_detail.html')
        # Статус код
        self.assertEqual(200, response.status_code)


class ContactCreateTest(BaseTestCase):
    '''Тесты для создания контактного лица компании'''

    def setUp(self):
        super().setUp()
        self.url = reverse('contact-create')
        # Пользователь с компанией
        self.client.force_login(self.user_with_company)


    def test_get_contact_create(self):
        '''Получение формы для создания контакта'''

        response = self.client.get(self.url)

        # Шаблон
        self.assertTemplateUsed(response, 'companies/contact_create.html')
        # Форма
        self.assertIsInstance(response.context['form'], ContactForm)
        # Статус код
        self.assertEqual(200, response.status_code)

        # Пользователь без компании
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        # Статус код
        self.assertEqual(404, response.status_code)


    def test_post_company_create(self):
        '''Отправка формы для создания контакта'''

        # Валидные данные для формы
        data = {
            'name': 'New Contact',
            'email': 'newcontact@mail.ru',
            'position': 'Manager',
            'phone_number': '128913'
        }
        response = self.client.post(self.url, data=data, follow=True)

        # Шаблон
        self.assertTemplateUsed(response, 'companies/contact_detail.html')
        # Cтатус код
        self.assertEqual(200, response.status_code)

        # Пользователь без компании
        self.client.force_login(self.user)
        response = self.client.post(self.url)
        # Статус код
        self.assertEqual(404, response.status_code)

# TODO: мб добавить тесты для ContactUpdateView (логика такая же что и в Create, мб нет смысла)
