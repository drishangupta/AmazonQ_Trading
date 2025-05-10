from django.urls import path
from . import views

urlpatterns = [
    path('', views.input_form, name='input_form'),
    path('submit-input/', views.input_form),
    path('kill-switch/', views.kill_switch),
    path('shutdown/', views.shutdown),
]
