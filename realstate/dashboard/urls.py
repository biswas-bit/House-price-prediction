from django.urls import path
from . import views

app_name = 'dashboard'
urlpatterns = [
    path ('model-prediction/', views.model_prediction, name='model_prediction'),
    path('data-input-form/', views.Data_input_form, name='data_input_form'),
    path('api/market-insights/',views.get_market_insights, name='market_insights'),
    path('api/get-recommendations/',views.get_recommendations,name='get_recommendations'),
]
