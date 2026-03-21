from django.urls import path
from . import views

app_name = "enrollments"

urlpatterns = [
    path("", views.home, name='home'),
    path("new-enrollment/", views.new_enrollment, name='new_enrollment'),
    path("enrollment-received/", views.enrollment_received, name='enrollment_received')
]