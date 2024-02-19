# Generated by Django 3.2.15 on 2023-06-07 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0041_orderitem_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('UNPROCESSED', 'Не обработан'), ('IN PROCESS', 'Собирается'), ('IN DELIVERY', 'Доставляется'), ('DONE', 'Выполнен')], db_index=True, default='UNPROCESSED', max_length=20, verbose_name='Статус заказа'),
        ),
    ]