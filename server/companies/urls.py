from django.urls import path
from companies.views import company_list, company_detail, company_create, company_edit


urlpatterns = [
    path('', company_list, name='company-list'),
    path('create/', company_create, name='company-create'),
    path('<int:company_id>/', company_detail, name='company-detail'),
    path('edit/', company_edit, name='company-edit'),
]
