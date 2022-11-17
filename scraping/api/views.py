import datetime
from rest_framework import filters
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from scraping.models import City, Language, Vacancy
from .serializers import *

period = datetime.date.today() - datetime.timedelta(1)


class DateFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        """
        request находится в self
        В данном случае не нужно self.request, потому что
        request передаётся в качестве параметра
        """
        city_slug = request.query_params.get('city', None)
        language_slug = request.query_params.get('language', None)
        return queryset.filter(
            city__slug=city_slug,
            language__slug=language_slug,
            timestamp__gte=period)


class CityViewSet(ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


class LanguageViewSet(ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


class VacancyViewSet(ModelViewSet):
    """
    ?city=moscow&language=python
    """
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    filter_backends = (DjangoFilterBackend, DateFilterBackend)
    filterset_fields = ('city__slug', 'language__slug')
    # По умолчанию ИЛИ. То есть или какой-то город или какой-то язык

    # def get_queryset(self):
    #     """
    #     query_params is GET in Django
    #     dict
    #     """
    #     city_slug = self.request.query_params.get('city', None)
    #     language_slug = self.request.query_params.get('language', None)
    #     qs = None
    #     if city_slug and language_slug:
    #         qs = Vacancy.objects.filter(
    #             city__slug=city_slug,
    #             language__slug=language_slug,
    #             timestamp__gte=period).select_related('city', 'language')  # (field__gte=5)  # field ≥ 5
            # if not qs.exists():
            #     qs = Vacancy.objects.filter(
            #         city__slug=language_slug,
            #         language__slug=city_slug,
            #         timestamp__gte=period).select_related('city', 'language')  # (field__gte=5)  # field ≥ 5
        # self.queryset = qs
        # return self.queryset

    #
    # def get_queryset(self):
    #     city_slug = self.request.query_params.get('city', None)
    #     language_slug = self.request.query_params.get('language', None)
    #     qs = None
    #     if city_slug and language_slug:
    #         city = City.objects.filter(slug=city_slug).first()
    #         language = Language.objects.filter(slug=language_slug).first()
    #         if city and language:
    #             qs = Vacancy.objects.filter(city=city, language=language,
    #                                         timestamp__gte=period).select_related('city', 'language')
    #     self.queryset = qs
    #     return self.queryset
    #
    #  # resp['result'][-1][''message]['chat']['id']