# Generated by Django 4.2.8 on 2023-12-19 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intel', '0015_alter_historicalprocessor_thermal_velocity_boost_frequency_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalprocessor',
            name='maximum_enclave_size_for_sgx',
            field=models.BigIntegerField(blank=True, help_text='How many bytes the Enclave Page Cache (EPC) can be.', null=True, verbose_name='Default Maximum Enclave Page Cache (EPC) Size for Intel SGX'),
        ),
        migrations.AlterField(
            model_name='processor',
            name='maximum_enclave_size_for_sgx',
            field=models.BigIntegerField(blank=True, help_text='How many bytes the Enclave Page Cache (EPC) can be.', null=True, verbose_name='Default Maximum Enclave Page Cache (EPC) Size for Intel SGX'),
        ),
    ]