# Generated by Django 4.2.5 on 2023-11-21 17:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_remove_deliveries_product_id_deliveries_product_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deliveries',
            name='product_id',
        ),
        migrations.RemoveField(
            model_name='deliveries',
            name='quantity',
        ),
        migrations.CreateModel(
            name='ProductInDelivery',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(default=0)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('status', models.CharField(default='Active', max_length=50)),
                ('delivery_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.deliveries')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
            ],
        ),
        migrations.AddField(
            model_name='deliveries',
            name='products',
            field=models.ManyToManyField(through='shop.ProductInDelivery', to='shop.product'),
        ),
    ]