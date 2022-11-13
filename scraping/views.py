from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse

from .models import Vacancy, City, Language
from .forms import FindForm, VacancyViewForm
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView


def home_view(request):
    form = FindForm()
    return render(request, 'scraping/home.html', {'form': form})


# def list_view(request):
#     """
#     For pagination: object_list instead of page_obj in html_file.
#     {% for obj in object_list %}
#     """
#     form = FindForm()
#     city = request.GET.get('city')
#     language = request.GET.get('language')
#     context = {
#         'city': city,
#         'language': language,
#         'form': form,
#     }
#     if city or language:
#         _filter = {}
#         if city:
#             _filter['city__slug'] = city
#             city_for_html = City.objects.filter(slug=_filter['city__slug']).first()
#             context['city_html'] = city_for_html
#         if language:
#             _filter['language__slug'] = language
#             language_for_html = Language.objects.filter(slug=_filter['language__slug']).first()
#             context['language_html'] = language_for_html
#         qs = Vacancy.objects.filter(**_filter).select_related('city', 'language')
#         paginator = Paginator(qs, 10)
#         page_number = request.GET.get('page')
#         page_obj = paginator.get_page(page_number)
#         context['object_list'] = page_obj
#     return render(request, 'scraping/list.html', context)


# def v_detail(request, pk=None):
#     # object_ = Vacancy.objects.get(pk=pk)
#     object_ = get_object_or_404(Vacancy, pk=pk)
#     return render(request, 'scraping/detail.html', {'object': object_})


class VacancyDetailView(DetailView):
    queryset = Vacancy.objects.all()
    template_name = 'scraping/detail.html'
    # context_object_name = 'object'

    slug_field = 'id'
    slug_url_kwarg = 'id'


class VacancyListView(ListView):
    model = Vacancy
    template_name = 'scraping/list.html'
    form = FindForm()
    paginate_by = 10
    # slug_field = 'id'
    # slug_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        """
        Default Value: context['object_list'] = Vacancy.objects.all()
        For pagination: page_obj instead of object_list in html_file.
        {% for obj in page_obj %}
        request is in self
        """
        context = super().get_context_data(**kwargs)
        city = self.request.GET.get('city')
        language = self.request.GET.get('language')
        context['city'] = city
        context['language'] = language
        context['form'] = self.form
        if city or language:
            _filter = {}
            if city:
                _filter['city__slug'] = city
                city_for_html = City.objects.filter(slug=_filter['city__slug']).first()
                context['city_html'] = city_for_html
            if language:
                _filter['language__slug'] = language
                language_for_html = Language.objects.filter(slug=_filter['language__slug']).first()
                context['language_html'] = language_for_html
        return context

    def get_queryset(self):
        city = self.request.GET.get('city')
        language = self.request.GET.get('language')
        qs = []
        if city or language:
            _filter = {}
            if city:
                _filter['city__slug'] = city
            if language:
                _filter['language__slug'] = language
            qs = Vacancy.objects.filter(**_filter).select_related('city', 'language')
        return qs


class VacancyCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Vacancy
    # fields = '__all__'          # One of the two
    form_class = VacancyViewForm  # One of the two
    template_name = 'scraping/create.html'
    success_message = 'The vacancy has been successfully created'
    success_url = reverse_lazy('home')


class VacancyUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Vacancy
    # fields = '__all__'          # One of the two
    form_class = VacancyViewForm  # One of the two
    template_name = 'scraping/create.html'
    # success_url = reverse_lazy('update', kwargs={'pk': })
    success_message = 'Information changed successfully'

    def get_success_url(self):
        vacancy_id = self.kwargs['id']
        return reverse_lazy('update', kwargs={'id': vacancy_id})

    slug_field = 'id'
    slug_url_kwarg = 'id'


class VacancyDeleteView(LoginRequiredMixin, DeleteView):
    model = Vacancy
    # template_name = 'scraping/delete.html'
    success_url = reverse_lazy('home')

    slug_field = 'id'
    slug_url_kwarg = 'id'

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        messages.success(request, 'The record was successfully deleted')
        return self.post(request, *args, **kwargs)

