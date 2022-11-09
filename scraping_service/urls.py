"""scraping_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from scraping import views
from scraping.views import VacancyDetailView, VacancyListView, VacancyCreateView, VacancyUpdateView, VacancyDeleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    # path('list/', views.list_view, name='list'),
    # path('detail/<int:pk>/', views.v_detail, name='detail'),

    path('detail/<slug:id>/', VacancyDetailView.as_view(), name='detail'),
    path('list/', VacancyListView.as_view(), name='list'),
    path('create/', VacancyCreateView.as_view(), name='create'),
    path('update/<slug:id>/', VacancyUpdateView.as_view(), name='update'),
    path('delete/<slug:id>/', VacancyDeleteView.as_view(), name='delete'),

    path('accounts/', include('accounts.urls')),
]
