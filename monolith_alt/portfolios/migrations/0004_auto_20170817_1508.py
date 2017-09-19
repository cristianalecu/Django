# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-17 12:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20170808_1509'),
        ('portfolios', '0003_auto_20170810_1306'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolioproduct',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='portfolioproduct',
            name='um',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='protfolio_products', to='shop.UnitMeasure'),
            preserve_default=False,
        ),
    ]