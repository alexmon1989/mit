from django.urls import path
from .views import photos, GalleryListView, like, GalleryDetailView

urlpatterns = [
    path('', GalleryListView.as_view(), name="photo_archive"),
    path('event/<int:pk>/', GalleryDetailView.as_view(), name="photo_archive_gallery"),
    path('photos.json', photos, name="photo_archive_photos_json"),
    path('like/', like, name="photo_archive_like"),
]
