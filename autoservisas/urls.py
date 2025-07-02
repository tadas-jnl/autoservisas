from django.urls import path, include
from . import views
urlpatterns = [
    # path('test/', views.test, name='test'),
    path('', views.index, name='index'),
    path('cars/', views.automobiliai, name='automobiliai'),
    path('cars/<int:car_id>', views.automobilis, name='automobilis'),
    path('orders/', views.OrderListView.as_view(), name="orders"),
    path('orders/<int:pk>', views.OrderDetailView.as_view(), name="order"),
    path('search/', views.search, name='search'),
    path('my_orders/', views.MyOrdersList.as_view(), name='my_orders'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name="profile"),
    path('add_order/', views.AddOrder.as_view(), name="add_order"),
    path('orders/<int:pk>/manage/', views.ManageOrder.as_view(), name='manage_order'),
    path('orders/<int:pk>/delete/', views.DeleteOrder.as_view(), name='delete_order')
]
