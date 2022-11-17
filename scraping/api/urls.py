from rest_framework import routers
from .views import *

app_name = 'api'

router = routers.DefaultRouter()
router.register('cities', CityViewSet)
router.register('languages', LanguageViewSet)
router.register('vacancy', VacancyViewSet)

urlpatterns = router.urls

