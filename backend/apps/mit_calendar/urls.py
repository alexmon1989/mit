from django.urls import path
from .views import EventListView, EventDetailView

urlpatterns = [
    path('', EventListView.as_view(), name="calendar_event_list"),
    path('event/<int:pk>/', EventDetailView.as_view(), name="calendar_event_detail"),
]
