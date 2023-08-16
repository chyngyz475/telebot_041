# Generated by Django 4.2.2 on 2023-08-09 12:25

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('telegram', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RetailOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Имя пользователя')),
                ('sku', models.CharField(max_length=255, verbose_name='Артикул товара')),
                ('color', models.CharField(max_length=255, verbose_name='Цвет товара')),
                ('size', models.CharField(max_length=255, verbose_name='Размер товара')),
                ('amount', models.FloatField()),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photos/')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Уникальный ID')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='telegram.status')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
    ]