from django.shortcuts import render
from .models import  RetailOrder, WholesaleOrderTelegtam 
from .models import Status
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import WholesaleOrderTelegtamSerializer, RetailOrderSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated 


class WholesaleApi(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WholesaleOrderTelegtamSerializer
    queryset = WholesaleOrderTelegtam.objects.all().order_by('id')

def wholesale_list(request):
    wholesale = WholesaleOrderTelegtam.objects.all()
    return render(request, 'orders.html', {'wholesales': wholesale})




class RetailApi(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RetailOrderSerializer 
    queryset = RetailOrder.objects.all().order_by('id')


def retail_list(request):
    orders = RetailOrder.objects.all()
    return render(request, 'applications.html', {'orders': orders})