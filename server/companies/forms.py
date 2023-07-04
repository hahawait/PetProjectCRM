from django import forms
from companies.models import Company, Contact


class CompanyForm(forms.ModelForm):
    '''Форма для компании'''
    class Meta:
        model = Company
        exclude = ['user']


class ContactForm(forms.ModelForm):
    '''Форма для контактного лица компании'''
    class Meta:
        model = Contact
        exclude = ['company', 'slug']
