from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from companies.models import Company
from companies.forms import CompanyForm
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
    if request.method == 'GET':
        context = {
            'form' : CompanyForm
        }
        return render(request, 'companies/company_create.html', context)
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            user = request.user
            if check_user_company(user):
                return HttpResponse('Вы можете добавить только одну компанию')
            else:
                company.user = user
                company.save()
                return redirect('company-list')


@login_required
def company_edit(request):
    '''Изменяет существующую компанию пользователя'''
    company = get_object_or_404(Company, user=request.user)
    if request.method == 'GET':
        form = CompanyForm(instance=company)
        # context = {
        #     'form': form,
        #     'company': company
        # }
        # return render(request, 'companies/company_edit.html', context)
    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect('company-list')

    context = {
        'form': form,
        'company': company
    }
    return render(request, 'companies/company_edit.html', context)
