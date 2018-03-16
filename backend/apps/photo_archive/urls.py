from django.urls import path
from .views import photos, PageView

urlpatterns = [
    path('', PageView.as_view(), name="photo_archive"),
    path('photos.json', photos, name="photo_archive_photos_json"),
]
