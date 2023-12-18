# Generated by Django 4.2.8 on 2023-12-17 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intel', '0013_alter_historicalprocessor_max_memory_speed_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalprocessor',
            name='deep_learning_boost_version',
            field=models.TextField(blank=True, help_text='The Intel Deep Learning Boost (Intel DL Boost) version the processor supports.', null=True, verbose_name='Intel Deep Learning Boost (Intel DL Boost) version'),
        ),
        migrations.AddField(
            model_name='processor',
            name='deep_learning_boost_version',
            field=models.TextField(blank=True, help_text='The Intel Deep Learning Boost (Intel DL Boost) version the processor supports.', null=True, verbose_name='Intel Deep Learning Boost (Intel DL Boost) version'),
        ),
    ]
