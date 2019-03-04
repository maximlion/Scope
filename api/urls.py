from django.urls import path

from .views import AcceptView

urlpatterns = [
    path('uploader/', AcceptView.as_view())
]
