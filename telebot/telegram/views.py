from django.shortcuts import render
from .models import  RetailOrder, WholesaleOrderTelegtam 
from django.shortcuts import render
from rest_framework import generics
from .models import WholesaleOrderTelegtam, RetailOrder
from .serializers import WholesaleOrderTelegtamSerializer, RetailOrderSerializer

class WholesaleOrderList(generics.ListAPIView):
    queryset = WholesaleOrderTelegtam.objects.all()
    serializer_class = WholesaleOrderTelegtamSerializer
    template_name = 'orders.html'  # The template to render

class RetailOrderList(generics.ListAPIView):
    queryset = RetailOrder.objects.all()
    serializer_class = RetailOrderSerializer
    template_name = 'applications.html'  # The template to render
            


def wholesale_list(request):
    wholesale = WholesaleOrderTelegtam.objects.all()
    return render(request, 'orders.html', {'wholesales': wholesale})


def retail_list(request):
    orders = RetailOrder.objects.all()
    return render(request, 'applications.html', {'orders': orders})


