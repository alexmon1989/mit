from django.urls import path
from .views import EventListView, EventDetailView, show_spectators

urlpatterns = [
    path('', EventListView.as_view(), name="calendar_event_list"),
    path('event/<int:pk>/', EventDetailView.as_view(), name="calendar_event_detail"),
    path('event/<int:pk>/spectators', show_spectators, name="calendar_event_spectators_list"),
]
