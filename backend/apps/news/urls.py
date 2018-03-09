from django.urls import path
from .views import NewsDetailView

urlpatterns = [
    path('event/<slug:slug>/', NewsDetailView.as_view(), name="news_detail"),
]
