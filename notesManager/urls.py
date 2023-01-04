from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("register", views.register_request, name="register"),
    path("create_note", views.create_note, name="create_note"),
]
