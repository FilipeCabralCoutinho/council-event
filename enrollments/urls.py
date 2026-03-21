from django.urls import path
import views

urlpatterns = [
    path("", views.home),
    path("new-enrollment/", views.new_enrollment),
    path("enrollment-received/", views.enrollment_received)
]