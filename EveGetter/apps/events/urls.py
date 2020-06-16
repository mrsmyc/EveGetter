from django.urls import path, re_path
from .views import (EventDetailView, EventDetailTicketBuy,
TicketBuy, MainPageListView, AllEventsDisplay,
EventLookUpCreator,
EventUpdateTickets,EventDetailView_true,
EventDetailTicketGift, TicketReturn,)
from . import views 
from django.conf.urls import url
from UsersProfiles.views import *
##TEST##
from .views import *


urlpatterns = [
    ####TEST#####
   # path('', EventList),
  # path("event_listing/", EventListing.as_view(), name='listing'),
   # path("ajax/event_type/", getEvent_type, name='get_event_type'),
  #  path("ajax/age/", getAge_start, name='get_age'),
   # path("ajax/date/", getDate, name='get_date'),
    ####TEST##########

    path('', views.MainPageListView,name='index'),
    path('events/all/',views.AllEventsDisplay, name='allevents'),
    path(r'^event/<int:pk>/$', views.EventDetailView_true, name='event-detail'),
    path('event/<int:pk>/redact/',views.UpdateEvent, name='event-redact'),
    path('event/<int:pk>/report/', views.EventLookReport, name='event-creator-report'),
    path('event/<int:pk>/creatorlook/', EventLookUpCreator, name='event-creator-detail'),
    # path('event/<int:pk>/creatorlook/', EventLookUpCreator.as_view(), name='event-creator-detail'),
    path('event/<int:pk>/tickets/create/',views.EventCreateTickets, name='create-tickets'),
    path('event/<int:pk>/tickets/update/', views.EventUpdateTickets, name='tickets-redact'),
    path('events/create/', views.createEvent, name='createEvent'),
    path('event/<int:pk>/tickets/gift', EventDetailTicketGift.as_view(), name='ticket-gift'),
    path('event/<int:pk>/tickets/buy/', EventDetailTicketBuy.as_view(), name='event-tickets-buy'),
    path('event/<int:pk>/tickets/gift/acc', views.TicketGiftDone, name='ticket-gift-acc'),
    path('event/<int:pk>/tickets/buy/done', views.TicketBuy, name='saveticket'),
    path('event/<int:pk>/tickets/alltickets', views.TicketAll, name='event-all-tickets'),
    path(r'^mytickets/<int:pk>/$',views.TicketReturn, name="ticket-return"),
    # path('myevents2/', artists_view, name='myevents_test'),

    
]