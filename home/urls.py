from django.urls import path, include
from home import views

urlpatterns = [
    path('', views.index, name='home'),
    path('upload_excel/', views.upload_excel, name='upload_excel'),
]
