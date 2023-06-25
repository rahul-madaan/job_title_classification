from django.urls import path, include
from home import views

urlpatterns = [
    path('', views.index, name='home'),
    path('upload_excel/', views.upload_excel, name='upload_excel'),
    path('train_model/', views.train_model, name='train_model'),
    path('get_predictions/', views.get_predictions, name='get_predictions'),
    path('download_excel/', views.download_excel, name='download_excel'),

]
