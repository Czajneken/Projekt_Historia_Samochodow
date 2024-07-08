from django.contrib.auth import get_user_model, login, logout
from django.contrib.staticfiles import finders
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import get_template
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView, ListView, UpdateView, DeleteView, TemplateView

from .forms import SearchCarReportForm, AddCarForm, AddCarOwnerForm, AddRepairForm
from .models import (
    BODY_TYPES,
    REPAIR_TYPES,
    FUEL_TYPES,
    Repair,
    Car,
    CarOwner,
    Events
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

            car = get_object_or_404(Car, number_of_the_registration_certificate__icontains=number_of_the_registration_certificate)
            # return redirect("car_report", car_id=car.pk)
            context |= {'car': car}

        return render(request, 'search_car_report.html', context)


def render_pdf_view(request, *args, **kwargs):
    car = get_object_or_404(Car, pk=kwargs['car_id'])
    template_path = 'pdf/pdf_car_report.html'
    context = {'car': car}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="raport_{car.plate_number}.pdf"'
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
        form = AddCarForm()
        context = {'form': form}
        return render(request, "add_car.html", context)

    def post(self, request, *args, **kwargs):
        form = AddCarForm(request.POST, request.FILES)
        context = {'form': form}
        if form.is_valid():
            brand = form.cleaned_data['brand']
            model = form.cleaned_data['model']
            color = form.cleaned_data['color']
            engine_size = form.cleaned_data['engine_size']
            engine_power_HP = form.cleaned_data['engine_power_HP']
            engine_power_kW = form.cleaned_data['engine_power_kW']
            mileage = form.cleaned_data['mileage']
            type_of_fuel = form.cleaned_data['type_of_fuel']
            body_type = form.cleaned_data['body_type']
            plate_number = form.cleaned_data['plate_number']
            VIN = form.cleaned_data['VIN']
            year_of_production = form.cleaned_data['year_of_production']
            date_of_first_registration = form.cleaned_data['date_of_first_registration']
            number_of_the_registration_certificate = form.cleaned_data['number_of_the_registration_certificate']
            car_photos = form.cleaned_data['car_photos']

            car = Car.objects.create(
                brand=brand,
                model=model,
                color=color,
                engine_size=engine_size,
                engine_power_HP=engine_power_HP,
                engine_power_kW=engine_power_kW,
                mileage=mileage,
                type_of_fuel=type_of_fuel,
                body_type=body_type,
                plate_number=plate_number,
                VIN=VIN,
                year_of_production=year_of_production,
                date_of_first_registration=date_of_first_registration,
                number_of_the_registration_certificate=number_of_the_registration_certificate,
                car_photos=car_photos,
            )
            # form.save()
            return redirect("mechanic")

        return render(request, "add_car.html", context)


class CarView(View):
    def get(self, request, *args, **kwargs):
        car = get_object_or_404(Car, pk=kwargs['car_id'])
        car_owner = get_object_or_404(CarOwner, car=kwargs['car_id'])
        context = {
            'car': car,
            'car_owner': car_owner,
        }
        return render(request, 'car.html', context)


class CarOwnerView(View):
    def get(self, request, *args, **kwargs):
        car_owner = get_object_or_404(CarOwner, pk=kwargs['car_owner_id'])
        context = {
            'car_owner': car_owner,
        }
        return render(request, 'car_owner.html', context)


class AddCarOwnerView(View):
    def get(self, request, *args, **kwargs):
        form = AddCarOwnerForm()
        context = {'form': form}
        return render(request, 'add_car_owner.html', context)

    def post(self, request, *args, **kwargs):
        form = AddCarOwnerForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            return redirect("mechanic")
        return render(request, 'add_car_owner.html', context)


class RepairView(View):
    def get(self, request, *args, **kwargs):
        repair = get_object_or_404(Repair, pk=kwargs['repair_id'])
        context = {
            'repair': repair,
        }
        return render(request, 'repair.html', context)


class AddRepairView(View):
    def get(self, request, *args, **kwargs):
        form = AddRepairForm()
        context = {'form': form}
        return render(request, 'add_repair.html', context)

    def post(self, request, *args, **kwargs):
        form = AddRepairForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            return redirect("mechanic")
        return render(request, 'add_repair.html', context)


class MechanicView(View):
    def get(self, request, *args, **kwargs):
        all_events = Events.objects.all()
        context = {
            "events": all_events,
        }
        return render(request, 'calendar.html', context)


class CalendarAllEventsView(View):
    def get(self, request, *args, **kwargs):
        all_events = Events.objects.all()
        out = []
        for event in all_events:
            out.append({
                'title': event.name,
                'pk': event.pk,
                'start': event.start.strftime("%m/%d/%Y, %H:%M:%S"),
                'end': event.end.strftime("%m/%d/%Y, %H:%M:%S"),
            })

        return JsonResponse(out, safe=False)


class CalendarAddEventView(View):
    def get(self, request, *args, **kwargs):
        start = request.GET.get("start", None)
        end = request.GET.get("end", None)
        title = request.GET.get("title", None)
        event = Events(name=str(title), start=start, end=end)
        event.save()
        data = {}
        return JsonResponse(data)


class CalendarUpdateEventView(View):
    def get(self, request, *args, **kwargs):
        start = request.GET.get("start", None)
        end = request.GET.get("end", None)
        title = request.GET.get("title", None)
        pk = request.GET.get("pk", None)
        event = Events.objects.get(pk=pk)
        event.start = start
        event.end = end
        event.name = title
        event.save()
        data = {}
        return JsonResponse(data)


class CalendarRemoveEventView(View):
    def get(self, request, *args, **kwargs):
        pk = request.GET.get("pk", None)
        event = Events.objects.get(pk=pk)
        event.delete()
        data = {}
        return JsonResponse(data)
