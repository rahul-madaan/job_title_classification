from django.urls import path
from home import views

urlpatterns = [
    path('', views.index, name='home'),
    path('upload_excel/', views.upload_excel, name='upload_excel'),
    path('train_model/', views.train_model, name='train_model'),
    path('get_predictions/', views.get_predictions, name='get_predictions'),
    path('download_excel/', views.download_excel, name='download_excel'),
    path('button_view/', views.button_view, name='button_view'),
    path('run_model/', views.run_model, name='run_model'),
    path('run_model_single/', views.run_model_single, name='run_model_single'),

]
