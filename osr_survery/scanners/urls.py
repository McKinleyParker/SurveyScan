from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/note_list/', views.PostNote.as_view()),
    path('api/property_list/', views.property_list),
    path('api/scan_list/', views.scan_list),
]