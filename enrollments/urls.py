from django.urls import path
from . import views

app_name = "enrollments"

urlpatterns = [
    path("", views.home, name='home'),
    path("new-enrollment/", views.new_enrollment, name='new_enrollment'),
    path('ajax/busca-igrejas/', views.busca_igrejas_por_distrito, name='ajax_busca_igrejas'),
    path("enrollment-received/", views.enrollment_received, name='enrollment_received'),
    path("dashboard/", views.dashboard, name='dashboard'),
    path("dashboard/export/", views.export_dashboard_excel, name='export_dashboard_excel')
]