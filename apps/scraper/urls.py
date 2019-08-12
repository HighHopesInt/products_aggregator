from django.urls import path
from django.contrib.auth.decorators import user_passes_test
from apps.scraper import views

urlpatterns = [
    path('',
         user_passes_test(lambda u: u.is_superuser)(views.chose_site_admin),
         name='scraper_sites')
]
