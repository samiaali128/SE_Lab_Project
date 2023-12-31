# Generated by Django 4.2.5 on 2023-09-24 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_review'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='product_id',
            new_name='product',
        ),
        migrations.AlterField(
            model_name='review',
            name='comment',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]),
        ),
    ]
