# Generated by Django 4.2.7 on 2023-11-29 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_eans_historicaleans'),
    ]

    operations = [
        migrations.AddField(
            model_name='eans',
            name='list_of_webhallen_ids_with_ean',
            field=models.TextField(blank=True, help_text='List of Webhallen IDs with EAN', null=True),
        ),
        migrations.AddField(
            model_name='historicaleans',
            name='list_of_webhallen_ids_with_ean',
            field=models.TextField(blank=True, help_text='List of Webhallen IDs with EAN', null=True),
        ),
    ]