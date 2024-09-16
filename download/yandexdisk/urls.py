from django.urls import path
from .views import IndexView, download_file



urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<str:public_key>/<str:file_path>', download_file, name='download_file'),
]