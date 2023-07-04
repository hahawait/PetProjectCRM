from django.urls import path
from companies.views import (company_list, company_detail, company_create, company_update,
                            ContactListView, ContactDetailView, ContactCreateView, ContactUpdateView
                        )


urlpatterns = [
    path('', company_list, name='company-list'),
    path('create/', company_create, name='company-create'),
    path('<int:company_id>/', company_detail, name='company-detail'),
    path('update/', company_update, name='company-update'),

    path('<int:company_id>/contacts/', ContactListView.as_view(), name='contact-list'),
    path('<int:company_id>/contacts/<slug:slug>/', ContactDetailView.as_view(), name='contact-detail'),
    path('contacts/create/', ContactCreateView.as_view(), name='contact-create'),
    path('contacts/<slug:slug>/update', ContactUpdateView.as_view(), name='contact-update'),

]
