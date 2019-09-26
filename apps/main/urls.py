from django.urls import path, re_path

from apps.main import views

urlpatterns = [

    path('', views.ProductList.as_view(), name='index'),

    re_path(r'^catalog/(?P<filter>.+)/$',
            views.ProductList.as_view(),
            name='catalog_filter'),

    re_path(r'^detail/(?P<pk>\d+)/$',
            views.ProductView.as_view(),
            name='product_detail'),

    path('products/', views.ProductApi.as_view()),
    path('products/<int:pk>', views.SingleProductAPI.as_view()),
    path('files/', views.FileUploadApi.as_view())
]
