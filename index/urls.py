from django.urls import path
from index import views


urlpatterns = [
    path('parser', views.parser),
    path('answer', views.answer),
]
