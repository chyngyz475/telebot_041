from django.contrib import admin
from .models import Application, Worker, Order
from .models import Status

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku')

admin.site.register(Application, ApplicationAdmin)

class StatusAdmin(admin.ModelAdmin):
    list_display = ('names',)

admin.site.register(Status, StatusAdmin)

class WorkerAdmin(admin.ModelAdmin):
    list_display = ('function',)

admin.site.register(Worker, WorkerAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ()

admin.site.register(Order, OrderAdmin)
