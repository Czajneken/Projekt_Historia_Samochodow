from django.contrib.auth import get_user_model, login, logout
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import get_template
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView, ListView, UpdateView, DeleteView, TemplateView

from .forms import SearchCarReportForm
from .models import (
    BODY_TYPES,
    REPAIR_TYPES,
    FUEL_TYPES,
    Repair,
    Car,
    CarOwner
)

from xhtml2pdf import pisa


class MainView(TemplateView):
    template_name = 'main.html'


class SearchCarReportView(View):
    def get(self, request, *args, **kwargs):
        form = SearchCarReportForm()
        context = {'form': form}
        return render(request, 'search_car_report.html', context)

    def post(self, request, *args, **kwargs):
        form = SearchCarReportForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            number_of_the_registration_certificate = form.cleaned_data['number_of_the_registration_certificate']

            car = Car.objects.all().filter(number_of_the_registration_certificate=number_of_the_registration_certificate)
            return redirect("car_report", car_id=car.pk)

        return render(request, 'search_car_report.html', context)


class CarReportView(View):
    def render_pdf_view(request, *args, **kwargs):
        car = get_object_or_404(Car, pk=kwargs['car_id'])
        template_path = 'pdf/pdf_car_report.html'
        context = {'car': car}
        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'filename="report_{car.plate_number}.pdf"'
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)

        # create a pdf
        pisa_status = pisa.CreatePDF(
            html, dest=response)
        # if error then show some funny view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response


class AddCarView(View):
    def get(self, request, *args, **kwargs):