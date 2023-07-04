from django.views import View
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404

from companies.models import Company, Contact
from companies.forms import CompanyForm, ContactForm
from companies.utils import check_user_company


def company_list(request):
    '''Рендерит шаблон со списком компаний, поиск по названию и адресу'''

    if request.method == 'GET':
        query_search = request.GET.get('q')
        if query_search:
            queryset= Company.objects.filter(
                Q(name__icontains=query_search) |
                Q(address__icontains=query_search))
        else:
            queryset = Company.objects.all()
        context = {
            'company_list': queryset,
            'query': query_search
        }
        return render(request, 'companies/company_list.html', context)


def company_detail(request, company_id):
    '''Рендерит шаблон компании'''

    if request.method == 'GET':
        company = get_object_or_404(Company, pk=company_id)
        return render(request, 'companies/company_detail.html', {'company': company})


@login_required
def company_create(request):
    '''Создает объект компании'''

    user = request.user
    if user.userrole.role == 'employer':
        if not check_user_company(user):
            if request.method == 'GET':
                return render(request, 'companies/company_create.html', {'form' : CompanyForm()})
            if request.method == 'POST':
                form = CompanyForm(request.POST)
                if form.is_valid():
                    company = form.save(commit=False)
                    company.user = user
                    company.save()
                    return redirect('company-list')
        else:
            return HttpResponse('Вы можете добавить только одну компанию')
    else:
        return HttpResponse('Только работадатели могут добавить компанию')


@login_required
def company_update(request):
    '''Изменяет существующую компанию пользователя'''
    user = request.user
    if user.userrole.role == 'employer':
        company = get_object_or_404(Company, user=request.user)
        if request.method == 'GET':
            form = CompanyForm(instance=company)
        if request.method == 'POST':
            form = CompanyForm(request.POST, instance=company)
            if form.is_valid():
                form.save()
                return redirect('company-list')
    else:
        return HttpResponse('Только работадатели могут изменить компанию')

    return render(request, 'companies/company_update.html', {'form': form})


class ContactListView(View):
    '''Список контактных лиц компании'''

    def get(self, request, company_id):
        '''Рендерит шаблон со списком контактных лиц компании'''

        queryset = get_list_or_404(Contact, company__id=company_id)
        return render(request, 'companies/contact_list.html', {'contact_list': queryset})


class ContactDetailView(View):
    '''Контактное лицо компании'''

    def get(self, request, company_id, slug):
        '''Рендерит шаблон с контактным лицом компании'''

        contact = get_object_or_404(Contact, company__id=company_id, slug=slug)
        return render(request, 'companies/contact_detail.html', {'contact': contact})


class ContactCreateView(LoginRequiredMixin, View):
    '''Создание контактного лица компании'''

    login_url = 'login'  # URL для перенаправления пользователя на страницу входа

    def get(self, request):
        '''Рендерит шаблон с формой, если у пользователя есть компания'''

        company = get_object_or_404(Company, user=request.user)
        return render(request, 'companies/contact_create.html', {'form': ContactForm()})


    def post(self, request):
        '''Добавляет контактное лицо, если у пользователя есть компания'''

        company = get_object_or_404(Company, user=request.user)
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.company = company
            contact.save()
            return redirect('contact-detail', company_id=company.id, slug=contact.slug)


class ContactUpdateView(View):
    '''Изменение контактного лица'''

    def get(self, request, slug):
        '''Получение формы, если пользователь - создатель объекта компании'''

        contact = get_object_or_404(Contact, slug=slug, company__user=request.user)
        form = ContactForm(instance=contact)
        return render(request, 'companies/contact_update.html', {'form': form})


    def post(self, request, slug):
        '''Изменение существующего контакного лица'''

        contact = get_object_or_404(Contact, slug=slug, company__user=request.user)
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.company = request.user.company
            contact.save()
            return redirect('contact-list', company_id=contact.company.id)
