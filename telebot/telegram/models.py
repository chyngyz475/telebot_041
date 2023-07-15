from django.utils import timezone
from django.db import models

class Status(models.Model):
    names = models.CharField(max_length=150, verbose_name='Статус',)

    def __str__(self) -> str:
        return str(self.names)
    
    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статус'

class Worker(models.Model):
    function = models.CharField(max_length=150, verbose_name='Работник',)

    def __str__(self) -> str:
        return str(self.function)
    
    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудник'

class Application(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Имя пользователя',
        )
    sku = models.CharField(
        max_length=255,
        verbose_name='Артикул товара',
        )
    color = models.CharField(
        max_length=255,
        verbose_name='Цвет товара',
        )
    size = models.CharField(
        max_length=255,
        verbose_name='Размер товара',
        )
    amount = models.FloatField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    photo = models.ImageField(
        upload_to='photos/', blank=True, null=True
        )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Order(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    amount = models.IntegerField()

    def __str__(self):
        return self.name


class Wholesale(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Имя пользователя',
        )
    sku = models.CharField(
        max_length=255,
        verbose_name='Артикул товара',
        )
    color = models.CharField(
        max_length=255,
        verbose_name='Цвет товара',
        )
    colorb = models.CharField(
        max_length=255,
        verbose_name='Цвет товара Б/У',
        )
    size = models.CharField(
        max_length=255,
        verbose_name='Размер товара',
        )
    amount = models.FloatField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    photo = models.ImageField(
        upload_to='photos/', blank=True, null=True
        )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'