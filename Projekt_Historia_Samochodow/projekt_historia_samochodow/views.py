from django.contrib.auth import get_user_model, login, logout
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, ListView, TemplateView

import json

from xhtml2pdf import pisa

from .forms import (
    SearchCarReportForm,
    AddCarForm,
    AddCarOwnerForm,
    AddRepairForm,
    LoginForm,
    UpdateCarMileageForm
)
from .models import (
    BODY_TYPES,
    REPAIR_TYPES,
    FUEL_TYPES,
    Repair,
    Car,
    CarOwner,
    Event
)

User = get_user_model()


class MainView(TemplateView):
    """
    Render App homepage's template.
    """
    template_name = 'main.html'


class SearchCarReportView(View):
    """
    Search a car in the DB by number of the registration certificate
    to generate a car report PDF file.
    """
    def get(self, request, *args, **kwargs):
        """
        Render a form to search a car in the DB.
        :param request: get
        :return: render template that includes form
        """
        form = SearchCarReportForm()
        context = {'form': form}
        return render(request, 'search_car_report.html', context)

    def post(self, request, *args, **kwargs):
        """
        Search a car in the DB by number of the registration certificate.
        If the data is valid you can genereate a car report PDF file.
        :param request: post
        :return: Car object from DB
        """
        form = SearchCarReportForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            number_of_the_registration_certificate = form.cleaned_data['number_of_the_registration_certificate']

            car = (get_object_or_404(
                Car, number_of_the_registration_certificate__icontains=number_of_the_registration_certificate))
            # return redirect("car_report", car_id=car.pk)
            context |= {'car': car}

        return render(request, 'search_car_report.html', context)


def render_pdf_view(request, *args, **kwargs):
    """
    Render a car report PDF file.
    :param request: get
    :param kwargs: car_id
    :return: Car report PDF file which contains all informations about the car
    """
    car = get_object_or_404(Car, pk=kwargs['car_id'])
    car_repairs = Repair.objects.filter(car=kwargs['car_id'])
    template_path = 'pdf/pdf_car_report.html'
    context = {
        'car': car,
        'car_repairs': car_repairs,
       }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # Display the PDF file in browser
    response['Content-Disposition'] = f'filename="raport_{car.plate_number}.pdf"'
    # Download the PDF file
    # response['Content-Disposition'] = 'attachment, filename="report.pdf"'
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
    """
    Add a car to the DB.
    """
    def get(self, request, *args, **kwargs):
        """
        Render a form to add a car to the DB.
        :param request: get
        :return: render template that includes form
        """
        form = AddCarForm()
        context = {'form': form}
        return render(request, "add_car.html", context)

    def post(self, request, *args, **kwargs):
        """
        Get the data from form and add a car to the DB.
        :param request: post
        :return: add a Car object to DB and redirect to Mechanic's homepage or raise form error
        """
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
    """
    Get and print a car, car's owner and car's repairs from DB.
    """
    def get(self, request, *args, **kwargs):
        """
        Get a car, car's owner and car's repairs from DB.
        :param request: get
        :param kwargs: car_id
        :return: Car, CarOwner, Repair objects from DB and render template that prints the data
        """
        car = get_object_or_404(Car, pk=kwargs['car_id'])
        car_owner = get_object_or_404(CarOwner, car=kwargs['car_id'])
        car_repairs = Repair.objects.filter(car=kwargs['car_id'])
        context = {
            'car': car,
            'car_owner': car_owner,
            'car_repairs': car_repairs,
        }
        return render(request, 'car.html', context)


class CarOwnerView(View):
    """
    Get and print car owner from DB.
    """
    def get(self, request, *args, **kwargs):
        """
        Get a car owner from DB.
        :param request: get
        :param kwargs: car_owner_id
        :return: CarOwner object and render template that prints the data
        """
        car_owner = get_object_or_404(CarOwner, pk=kwargs['car_owner_id'])
        context = {
            'car_owner': car_owner,
        }
        return render(request, 'car_owner.html', context)


class AddCarOwnerView(View):
    """
    Add a car owner to DB.
    """
    def get(self, request, *args, **kwargs):
        """
        Render a form to add a car owner to DB.
        :param request: get
        :return: render template that includes form
        """
        form = AddCarOwnerForm()
        context = {'form': form}
        return render(request, 'add_car_owner.html', context)

    def post(self, request, *args, **kwargs):
        """
        Get the data from form and add a car owner to DB.
        :param request: post
        :return: add a CarOwner object to DB and redirect to Mechanic's homepage or raise form error
        """
        form = AddCarOwnerForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            return redirect("mechanic")
        return render(request, 'add_car_owner.html', context)


class RepairView(View):
    """
    Get and print a car's repairs from DB.
    """
    def get(self, request, *args, **kwargs):
        """
        Get and print a car and car's repairs from DB.
        :param request: get
        :param kwargs: car_id, repair_id
        :return: Car and Repair objects from DB and render template that prints the data
        """
        car_pk = kwargs['car_id']
        repair_pk = kwargs['repair_id']

        car = get_object_or_404(Car, pk=car_pk)
        repair = get_object_or_404(Repair, pk=repair_pk)

        context = {
            'car': car,
            'repair': repair,
        }
        return render(request, 'repair.html', context)


class AddRepairView(View):
    """
    Add a car's repair to DB.
    """
    def get(self, request, *args, **kwargs):
        """
        Render a form to add a car's repair to DB.
        :param request: get
        :return: render template that includes form
        """
        form = AddRepairForm()
        context = {'form': form}
        return render(request, 'add_repair.html', context)

    def post(self, request, *args, **kwargs):
        """
        Get the data from form and add a car's repair to DB.
        Get the car.pk from 'car' form field to correctly redirect.
        :param request: post
        :return: add a Repair object to DB, get car.pk and redirect to URL 'update_mileage' or raise form error
        """
        form = AddRepairForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            car_pk = form.cleaned_data['car'].pk
            form.save()
            return redirect("update_mileage", car_id=car_pk)
        return render(request, 'add_repair.html', context)


class MechanicView(View):
    """
    Render Mechanic's homepage.
    """
    def get(self, request, *args, **kwargs):
        """
        Render Mechanic's homepage.
        :param request: get
        :return: render template
        """
        return render(request, 'mechanic_site.html')


# class CalendarAllEventsView(View):
#     def get(self, request, *args, **kwargs):
#         events = Event.objects.all()
#         events_list = []
#         for event in events:
#             events_list.append({
#                 'id': event.id,
#                 'title': event.title,
#                 'start': event.start.isoformat(),
#                 'end': event.end.isoformat() if event.end else None,
#                 'description': event.description,
#             })
#         return JsonResponse(events_list, safe=False)
#
#
# class CalendarAddEventView(View):
#     def add_event(request):
#         if request.method == "POST":
#             data = json.loads(request.body)
#             title = data.get('title')
#             start = data.get('start')
#             end = data.get('end')
#             description = data.get('description')
#             if title and start:
#                 event = Event.objects.create(title=title, start=start, end=end, description=description)
#                 return JsonResponse(
#                        {
#                        'id': event.id,
#                        'title': event.title,
#                        'start': event.start,
#                        'end': event.end,
#                        'description': event.description
#                        })
#         return HttpResponseBadRequest("Invalid request")
#
#
# class CalendarUpdateEventView(View):
#     def update_event(request, event_id):
#         try:
#             event = Event.objects.get(id=event_id)
#         except Event.DoesNotExist:
#             return HttpResponseBadRequest("Event not found")
#
#         if request.method == "POST":
#             data = json.loads(request.body)
#             event.title = data.get('title', event.title)
#             event.start = data.get('start', event.start)
#             event.end = data.get('end', event.end)
#             event.description = data.get('description', event.description)
#             event.save()
#             return JsonResponse(
#                    {'id': event.id,
#                    'title': event.title,
#                    'start': event.start,
#                    'end': event.end,
#                    'description': event.description
#                    })
#
#         return HttpResponseBadRequest("Invalid request")
#
#
# class CalendarDeleteEventView(View):
#     def delete_event(request, event_id):
#         try:
#             event = Event.objects.get(id=event_id)
#         except Event.DoesNotExist:
#             return HttpResponseBadRequest("Event not found")
#
#         if request.method == "DELETE":
#             event.delete()
#             return JsonResponse({"status": "deleted"})
#
#         return HttpResponseBadRequest("Invalid request")


class LoginView(FormView):
    """
    Render login form, log in user and redirect to Mechanic's homepage or raise login error.
    """
    form_class = LoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('mechanic')


class LogoutView(View):
    """
    Log out user and redirect to the App's homepage.
    """
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('main')


class CarListView(ListView):
    """
    Return a list of all cars.
    """
    model = Car
    template_name = "car_list.html"


class CarOwmerListView(ListView):
    """
    Return a list of all car owmers.
    """
    model = CarOwner
    template_name = "car_owner_list.html"


class CarMileageUpdate(View):
    """
    Update car's mileage.
    """
    def get(self, request, *args, **kwargs):
        """
        Render a form to update car's mileage.
        :param request: get
        :param kwargs: car_id
        :return: Car object from DB and render template that includes form
        """
        car_pk = kwargs['car_id']
        car = get_object_or_404(Car, pk=car_pk)
        form = UpdateCarMileageForm
        context = {
            'form': form,
            'car': car,
        }
        return render(request, "car_mileage_update_form.html", context)

    def post(self, request, *args, **kwargs):
        """
        Get the data from form and update car's mileage.
        :param request: post
        :param kwargs: car_id
        :return: Car object from DB, update car.mileage and redirect to Mechanic's homepage or raise form error
        """
        car_pk = kwargs['car_id']
        car = get_object_or_404(Car, pk=car_pk)
        form = UpdateCarMileageForm(request.POST)
        context = {
            'form': form,
            'car': car,
        }
        if form.is_valid():
            mileage = form.cleaned_data['mileage']
            car.mileage = mileage
            car.save()
            return redirect("mechanic")
        return render(request, 'car_mileage_update_form.html', context)


def calendar_view(request):
    """
    Render fullcalendar.js's template.
    :param request: get
    :return: render template
    """
    return render(request, 'calendar.html')


def events_json(request):
    """
    Get events from DB.
    :param request: get
    :return: Event objects from DB
    """
    events = Event.objects.all()
    events_list = []
    for event in events:
        events_list.append({
            'id': event.id,
            'title': event.title,
            'start': event.start.isoformat(),
            'end': event.end.isoformat() if event.end else None,
        })
    return JsonResponse(events_list, safe=False)


def add_event(request):
    """
    Add event to DB.
    :param request: post
    :return: add Event object to DB or raise error
    """
    if request.method == "POST":
        data = json.loads(request.body)
        title = data.get('title')
        start = data.get('start')
        end = data.get('end')
        if title and start:
            event = Event.objects.create(title=title, start=start, end=end)
            return JsonResponse({'id': event.id, 'title': event.title, 'start': event.start, 'end': event.end})
    return HttpResponseBadRequest("Invalid request")


def delete_event(request, event_id):
    """
    Delete event from DB.
    :param request: delete
    :param event_id: event.pk
    :return: delete Event object from DB
    """
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return HttpResponseBadRequest("Event not found")

    if request.method == "DELETE":
        event.delete()
        return JsonResponse({"status": "deleted"})

    return HttpResponseBadRequest("Invalid request")


class UserListView(ListView):
    """
    Return a user list.
    """
    model = User
    template_name = 'user_list.html'
    context_object_name = 'users'
