from django.urls import path
from .views import PlayDetailView

urlpatterns = [
    path('', PlayDetailView.as_view(), name="play"),
]
