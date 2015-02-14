from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from references.forms import CreateReferenceForm
from references.models import Reference


class CreateReferenceView(CreateView):
    model = Reference
    form_class = CreateReferenceForm
    template_name = 'references/create_reference.html'


class ReferencesListView(ListView):
    model = Reference
    template_name = 'references/list_references.html'


class ReferenceDetailView(DetailView):
    model = Reference
    template_name = 'references/detail_reference.html'
