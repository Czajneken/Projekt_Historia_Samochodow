from django.urls import path
from .views import render_pdf_view

app_name = 'projekt_historia_samochodow'

urlpatterns = [
    path('pdf/<int:car_id>/', render_pdf_view, name='pdf_car_report'),
]