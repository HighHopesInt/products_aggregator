from django.urls import path

from apps.stats import views

urlpatterns = [
    path('', views.stats, name='stats')
]
