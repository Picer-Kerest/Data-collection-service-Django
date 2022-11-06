from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Vacancy, City, Language
from .forms import FindForm


def home_view(request):
    form = FindForm()
    return render(request, 'scraping/home.html', {'form': form})


def list_view(request):
    form = FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    context = {
        'city': city,
        'language': language,
        'form': form,
    }
    if city or language:
        _filter = {}
        if city:
            _filter['city__slug'] = city
            city_for_html = City.objects.filter(slug=_filter['city__slug']).first()
            context['city'] = city_for_html
        if language:
            _filter['language__slug'] = language
            language_for_html = Language.objects.filter(slug=_filter['language__slug']).first()
            context['language'] = language_for_html
        qs = Vacancy.objects.filter(**_filter)
        paginator = Paginator(qs, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['object_list'] = page_obj
    return render(request, 'scraping/list.html', context)


