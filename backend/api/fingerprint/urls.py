from django.urls import path

from api.fingerprint import views

urlpatterns = [path("", views.FingerPrint.as_view())]
