# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-05 00:34
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stellar', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StellarTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.TextField(unique=True)),
                ('from_address', models.TextField()),
                ('to_address', models.TextField()),
                ('amount', models.FloatField()),
                ('source_account', models.TextField()),
                ('type', models.TextField()),
                ('type_i', models.IntegerField()),
                ('asset_type', models.TextField()),
                ('transaction_hash', models.TextField()),
                ('created_at', models.DateTimeField()),
                ('receiver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stellar_received', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stellar_sent', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='stellartransaction',
            unique_together=set([('identifier', 'sender', 'receiver')]),
        ),
    ]