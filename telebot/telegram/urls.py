from django.urls import path, include
from . import views

urlpatterns = [
    # other URL patterns
    path('application', views.retail_list, name='application'),
    path('orders/', views.wholesale_list, name='orders'),
    path('api/wholesale', views.WholesaleApi.as_view()),
    path('api/retail', views.RetailApi.as_view()),
]
