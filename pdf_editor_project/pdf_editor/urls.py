from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_pdf, name='upload_pdf'),
    path('convert_back/', views.convert_back_to_pdf, name='convert_back_to_pdf'),
]
