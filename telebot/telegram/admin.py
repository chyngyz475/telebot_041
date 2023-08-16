from django.contrib import admin
from .models import Worker, WholesaleOrderTelegtam,RetailOrder
from .models import Status

class StatusAdmin(admin.ModelAdmin):
    list_display = ('names',)

admin.site.register(Status, StatusAdmin)

class WorkerAdmin(admin.ModelAdmin):
    list_display = ('function',)

admin.site.register(Worker, WorkerAdmin)



class WholesaleOrderTelegtamAdmin(admin.ModelAdmin):
    list_display = ('username', 'quantity', 'item_sku', 'item_color', 'item_size', 'amount', 'photowh', 'status', 'created_at', 'unique_id')

admin.site.register(WholesaleOrderTelegtam, WholesaleOrderTelegtamAdmin)

class RetailOrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'color', 'size', 'amount', 'photo', 'status', 'created_date', 'unique_id')
admin.site.register(RetailOrder, RetailOrderAdmin)