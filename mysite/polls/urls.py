from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('submit-query', views.submit_query)
]