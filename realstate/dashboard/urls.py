from django.urls import path
from . import views

app_name = 'dashboard'
urlpatterns = [
    path ('model-prediction/', views.model_prediction, name='model_prediction'),
    path('data-input-form/', views.Data_input_form, name='data_input_form'),
]
