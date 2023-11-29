# Generated by Django 4.2.7 on 2023-11-29 20:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0009_alter_historicalsitemaparticle_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Eans',
            fields=[
                ('ean', models.TextField(help_text='EAN', primary_key=True, serialize=False)),
                ('name', models.TextField(blank=True, help_text='Product name', null=True)),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Created')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Updated')),
            ],
            options={
                'verbose_name': 'European Article Number',
                'verbose_name_plural': 'European Article Numbers',
                'db_table': 'eans',
            },
        ),
        migrations.CreateModel(
            name='HistoricalEans',
            fields=[
                ('ean', models.TextField(db_index=True, help_text='EAN')),
                ('name', models.TextField(blank=True, help_text='Product name', null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical European Article Number',
                'verbose_name_plural': 'historical European Article Numbers',
                'db_table': 'eans_history',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
