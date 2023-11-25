from django.urls import path
from . import views

urlpatterns = [
    # other URL patterns
    path('application', views.retail_list, name='application'),
    path('orders/', views.wholesale_list, name='orders'),
    path('api/wholesale/', views.WholesaleOrderList.as_view(), name='wholesale-list'),
    path('api/retail/', views.RetailOrderList.as_view(), name='retail-list'),
]
