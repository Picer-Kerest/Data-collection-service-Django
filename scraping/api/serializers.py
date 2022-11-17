from rest_framework.serializers import ModelSerializer
from scraping.models import City, Language, Vacancy


class CitySerializer(ModelSerializer):

    class Meta:
        model = City
        fields = ('name', 'slug')


class LanguageSerializer(ModelSerializer):

    class Meta:
        model = Language
        fields = ('name', 'slug')


class VacancySerializer(ModelSerializer):

    class Meta:
        model = Vacancy
        fields = '__all__'
