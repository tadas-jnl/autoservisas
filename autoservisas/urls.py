from django.urls import path
from . import views
urlpatterns = [
    # path('test/', views.test, name='test'),
    path('', views.index, name='index'),
    path('cars/', views.automobiliai, name='automobiliai'),
    path('cars/<int:car_id>', views.automobilis, name='automobilis'),
]