from django.views.generic.edit import CreateView

from companies.models import Company


class CreateCompanyView(CreateView):
    model = Company
    template_name = 'company_create.html'

