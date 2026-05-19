"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

admin.site.site_header = 'Painel de Administração do Concílio 6ª Região'
admin.site.site_title = 'Painel de Administração do Concílio 6ª Região'
admin.site.index_title = 'Administração do Sistema'

urlpatterns = [
    path('', RedirectView.as_view(url='/enrollments/', permanent=True)),
    path('admin/', admin.site.urls),
    path('enrollments/', include('enrollments.urls')),
    path('plenary_control/', include('plenary_control.urls'))
]
