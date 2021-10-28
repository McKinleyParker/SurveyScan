from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/property_list/', views.property_list)
]