"""
URL configuration for SmartFarm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.urls import path

from app import views

urlpatterns = [
    path("first/", views.first, name="first"),
    path("home/", views.home, name="home"),
    path("dispositivos/", views.dispositivos, name="dispositivos"),
    path("sensores/", views.sensores, name="sensores"),
    path("relatorio/", views.relatorio, name="relatorio"),
    path('dispositivos/delete/<int:dispositivo_id>/', views.delete_dispositivo, name='delete_dispositivo'),
    path('dispositivos/atualizar/<int:dispositivo_id>/', views.atualizar_dispositivo, name='atualizar_dispositivo'),
    path('dispositivos/adicionar/', views.adicionar_dispositivo, name='adicionar_dispositivo')

]
