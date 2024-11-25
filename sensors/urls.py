from django.urls import path
from . import views

urlpatterns = [
    path('sensor_acquisitions/', views.sensor_acquisitions, name='sensor_acquisitions'),
    path('sensor_last_acquisition/<str:platform_id>/', views.sensor_last_acquisition, name='sensor_last_acquisition'),
]
