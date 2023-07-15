from django.shortcuts import render
from .models import Application
from .models import Status,Wholesale
from telegram.models import Order
from django.core.paginator import Paginator

def orders_view(request):
    orders = Order.objects.all()
    return render(request, 'orders.html', {'orders': orders})

def Core(request):
    applications = Application.objects.all()
    status = Status.objects.all()
    paginator = Paginator(applications, 10)


    page_number = request.GET.get('page')  # Get the current page number from the request
    page_obj = paginator.get_page(page_number)

    context = {
        'applications': applications,
        'status' : status,
        'page_obj': page_obj,

    }
    return render(request, 'applications.html',context=context)

def wholesale_view(request):
    applications = Application.objects.all()
    status = Status.objects.all()
    paginator = Paginator(applications, 10)
    wholesale = Wholesale.objects.all()

    page_number = request.GET.get('page')  # Get the current page number from the request
    page_obj = paginator.get_page(page_number)

    context = {
        'applications': applications,
        'status' : status,
        'page_obj': page_obj,
        'wholesale': wholesale

    }
    return render(request, 'wholesale.html',context=context)

