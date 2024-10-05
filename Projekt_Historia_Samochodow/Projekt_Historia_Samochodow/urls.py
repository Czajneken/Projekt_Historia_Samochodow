"""
URL configuration for Projekt_Historia_Samochodow project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from projekt_historia_samochodow import views as phs_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', phs_views.MainView.as_view(), name='main'),
    path('search_car_report/', phs_views.SearchCarReportView.as_view(), name='search_car_report'),
    path('car_report/', include('projekt_historia_samochodow.urls'), name='car_report'),
    path('car/<int:car_id>/', phs_views.CarView.as_view(), name='car'),
    path('add_car', phs_views.AddCarView.as_view(), name='add_car'),
    path('car_owner/<int:car_owner_id>/', phs_views.CarOwnerView.as_view(), name='car_owner'),
    path('add_car_owner', phs_views.AddCarOwnerView.as_view(), name='add_car_owner'),
    path('repair/<int:car_id>/<int:repair_id>', phs_views.RepairView.as_view(), name='repair'),
    path('add_repair/', phs_views.AddRepairView.as_view(), name='add_repair'),
    path('calendar/', phs_views.calendar_view, name='calendar'),
    path('api/events/', phs_views.events_json, name='events_json'),
    path('api/events/add/', phs_views.add_event, name='add_event'),
    path('api/events/delete/<int:event_id>/', phs_views.delete_event, name='delete_event'),
    path('mechanic', phs_views.MechanicView.as_view(), name='mechanic'),
    # path('all_events', phs_views.CalendarAllEventsView.as_view(), name='all_events'),
    # path('add_event', phs_views.CalendarAddEventView.as_view(), name='add_event'),
    # path('update_event/<int:event_id>', phs_views.CalendarUpdateEventView.as_view(), name='update_event'),
    # path('remove_event/<int:event_id>', phs_views.CalendarDeleteEventView.as_view(), name='delete_event'),
    path('login', phs_views.LoginView.as_view(), name='login'),
    path('logout', phs_views.LogoutView.as_view(), name='logout'),
    path('car_list', phs_views.CarListView.as_view(), name='car_list'),
    path('car_owner_list', phs_views.CarOwmerListView.as_view(), name='car_owner_list'),
    path('update_mileage/<int:car_id>', phs_views.CarMileageUpdate.as_view(), name='update_mileage'),
    path('user_list', phs_views.UserListView.as_view(), name='user_list')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
