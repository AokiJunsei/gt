from django.urls import path

from . import views

app_name = 'gt'
urlpatterns = [
    path('', views.IndexViews.as_view(), name="top")
]