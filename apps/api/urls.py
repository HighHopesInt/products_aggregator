from django.urls import path

from apps.api import views

urlpatterns = [
    path('products/', views.ProductApi.as_view()),
    path('products/<int:pk>', views.SingleProductAPI.as_view()),
    path('files/', views.FileUploadApi.as_view())
]
