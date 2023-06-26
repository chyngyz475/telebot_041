from django.urls import path
from . import views
from telegram.views import orders_view
urlpatterns = [
    # other URL patterns
    path('', views.Core, name='core'),
    path('orders/', orders_view, name='orders'),
]