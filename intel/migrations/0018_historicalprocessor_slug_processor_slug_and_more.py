# Generated by Django 4.2.8 on 2024-01-04 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intel', '0017_rename_maximum_turbo_power_historicalprocessor_max_turbo_power_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalprocessor',
            name='slug',
            field=models.SlugField(blank=True, help_text='Slug used for the URL.', null=True, verbose_name='Slug'),
        ),
        migrations.AddField(
            model_name='processor',
            name='slug',
            field=models.SlugField(blank=True, help_text='Slug used for the URL.', null=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='historicalprocessor',
            name='name',
            field=models.TextField(default='Unknown', help_text='The name of the processor.', verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='processor',
            name='name',
            field=models.TextField(default='Unknown', help_text='The name of the processor.', verbose_name='Name'),
        ),
    ]
