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
    path("dispositivos_e_sensores/", views.dispositivos,
         name="dispositivos_e_sensores"),
    path("relatorio/", views.relatorio, name="relatorio"),
    path('dispositivos/delete/<int:dispositivo_id>/',
         views.delete_dispositivo, name='delete_dispositivo'),
    path('dispositivos/atualizar/<int:dispositivo_id>/',
         views.atualizar_dispositivo, name='atualizar_dispositivo'),
    path('dispositivos/adicionar/', views.adicionar_dispositivo,
         name='adicionar_dispositivo'),
    path('sensores/delete/<int:sensor_id>/',
         views.delete_sensor, name='delete_sensor'),
    path('sensores/atualizar/<int:sensor_id>/',
         views.atualizar_sensor, name='atualizar_sensor'),
    path('sensores/adicionar/<int:dispositivo_id>/',
         views.adicionar_sensor, name='adicionar_sensor'),
    path('mostrarelatorio', views.mostrarelatorio, name='mostrarelatorio'),
    path('publish', views.publish_message, name='publish'),

]
