# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-26 10:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0004_auto_20160107_1755'),
        ('catalogue', '0009_slugfield_noop'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='partner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='productPartner', to='partner.Partner', verbose_name='Partner'),
        ),
    ]