from django import forms
from companies.models import Company, Contact


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ['user']


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ['company', 'slug']
