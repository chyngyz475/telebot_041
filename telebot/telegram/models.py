
from django.utils import timezone
import uuid
from django.db import models

class Status(models.Model):
    names = models.CharField(max_length=150, verbose_name='Статус',)

    def __str__(self) -> str:
        return str(self.names)
    
    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статус'

class Worker(models.Model):
    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудник'

    function = models.CharField(max_length=150, verbose_name='Работник',)
    def __str__(self) -> str:
        return str(self.function)
    


    

class WholesaleOrderTelegtam(models.Model):
    class Meta:
        verbose_name = 'ЗаказОптом'
        verbose_name_plural = 'ЗаказыОптом'

    # Existing fields
    username = models.TextField(verbose_name='Имя пользователя')
    quantity = models.IntegerField()
    item_sku = models.TextField(verbose_name='Артикул товара')
    item_color = models.TextField(verbose_name='Color')
    item_size = models.TextField(verbose_name='Размер товара')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    photowh = models.ImageField(upload_to='photos/', blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    
    # New fields
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Уникальный ID')

    def __str__(self):
        return str(self.username)
    



class RetailOrder(models.Model):
    class Meta:
        verbose_name = 'ТоварРозницу'
        verbose_name_plural = 'ТоварРозницу'

    # Existing fields
    name = models.CharField(max_length=255, verbose_name='Имя пользователя')
    sku = models.CharField(max_length=255, verbose_name='Артикул товара')
    color = models.CharField(max_length=255, verbose_name='Цвет товара')
    size = models.CharField(max_length=255, verbose_name='Размер товара')
    amount = models.FloatField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    adds = models.TextField(verbose_name='Адрес доставки')
    # New fields
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    id_wh = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Уникальный IDwh')

    def __str__(self) -> str:
        return str(self.name)
    

class UserProfile(models.Model):
    user_id = models.BigIntegerField(unique=True)
    phone_number = models.CharField(max_length=15)  # Adjust max_length as needed
    # Add other fields as needed

    def __str__(self):
        return f"User {self.user_id}"