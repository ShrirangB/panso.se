# Generated by Django 4.2.7 on 2023-11-23 22:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebhallenProduct',
            fields=[
                ('product_id', models.IntegerField(help_text='Product ID', primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Created')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Updated')),
                ('minimum_rank_level', models.IntegerField(blank=True, help_text='Minimum rank level', null=True)),
                ('images', models.TextField(blank=True, help_text='Comma separated image URLs')),
                ('name', models.TextField(blank=True, help_text='Product name')),
                ('price', models.TextField(blank=True, help_text='Product price')),
                ('vat', models.TextField(blank=True, help_text='Product VAT')),
                ('price_end_at', models.DateTimeField(blank=True, help_text='Price end at', null=True)),
                ('price_nearly_over', models.BooleanField(default=False, help_text='Price nearly over')),
                ('price_flash_sale', models.BooleanField(default=False, help_text='Price flash sale')),
                ('price_type', models.TextField(blank=True, help_text='Price type')),
                ('regular_price', models.TextField(blank=True, help_text='Regular price')),
                ('regular_price_type', models.TextField(blank=True, help_text='Regular price type')),
                ('regular_price_end_at', models.DateTimeField(blank=True, help_text='Regular price end at', null=True)),
                ('regular_price_nearly_over', models.BooleanField(default=False, help_text='Regular price nearly over')),
                ('regular_price_flash_sale', models.BooleanField(default=False, help_text='Regular price flash sale')),
                ('lowest_price', models.TextField(blank=True, help_text='Lowest price')),
                ('lowest_price_type', models.TextField(blank=True, help_text='Lowest price type')),
                ('lowest_price_end_at', models.DateTimeField(blank=True, help_text='Lowest price end at', null=True)),
                ('lowest_price_nearly_over', models.BooleanField(default=False, help_text='Lowest price nearly over')),
                ('lowest_price_flash_sale', models.BooleanField(default=False, help_text='Lowest price flash sale')),
                ('level_one_price', models.TextField(blank=True, help_text='Level one price')),
                ('level_one_price_type', models.TextField(blank=True, help_text='Level one price type')),
                ('level_one_price_end_at', models.DateTimeField(blank=True, help_text='Level one price end at', null=True)),
                ('level_one_price_nearly_over', models.BooleanField(default=False, help_text='Level one price nearly over')),
                ('level_one_price_flash_sale', models.BooleanField(default=False, help_text='Level one price flash sale')),
                ('description', models.TextField(blank=True, help_text='Product description')),
                ('meta_title', models.TextField(blank=True, help_text='Product meta title')),
                ('meta_description', models.TextField(blank=True, help_text='Product meta description')),
                ('canonical_url', models.TextField(blank=True, help_text='Product canonical URL')),
                ('release_date', models.DateTimeField(blank=True, help_text='Product release date', null=True)),
                ('section_id', models.IntegerField(blank=True, help_text='Section ID', null=True)),
                ('is_digital', models.BooleanField(default=False, help_text='Is digital')),
                ('discontinued', models.BooleanField(default=False, help_text='Discontinued')),
                ('category_tree', models.TextField(blank=True, help_text='Category tree')),
                ('main_category_path', models.TextField(blank=True, help_text='Comma separated main category path')),
                ('manufacturer', models.IntegerField(blank=True, help_text='Manufacturer', null=True)),
                ('part_numbers', models.TextField(blank=True, help_text='Comma separated list of part numbers')),
                ('eans', models.TextField(blank=True, help_text='Comma separated list of EANs')),
                ('thumbnail', models.TextField(blank=True, help_text='Thumbnail URL')),
                ('average_rating', models.FloatField(blank=True, help_text='Average rating', null=True)),
                ('average_rating_type', models.TextField(blank=True, help_text='Average rating type')),
                ('energy_marking', models.TextField(blank=True, help_text='Energy marking')),
                ('package_size_id', models.IntegerField(blank=True, help_text='Package size ID', null=True)),
                ('status_codes', models.TextField(blank=True, help_text='Comma separated list of status codes')),
                ('long_delivery_notice', models.TextField(blank=True, help_text='Long delivery notice')),
                ('categories', models.TextField(blank=True, help_text='Comma separated list of categories')),
                ('phone_subscription', models.BooleanField(default=False, help_text='Phone subscription')),
                ('highlighted_review_id', models.IntegerField(blank=True, help_text='Highlighted review ID', null=True)),
                ('highlighted_review_text', models.TextField(blank=True, help_text='Highlighted review text')),
                ('highlighted_review_rating', models.IntegerField(blank=True, help_text='Highlighted review rating', null=True)),
                ('highlighted_review_upvotes', models.IntegerField(blank=True, help_text='Highlighted review upvotes', null=True)),
                ('highlighted_review_downvotes', models.IntegerField(blank=True, help_text='Highlighted review downvotes', null=True)),
                ('highlighted_review_verified', models.BooleanField(default=False, help_text='Highlighted review verified')),
                ('highlighted_review_created', models.DateTimeField(blank=True, help_text='Highlighted review created', null=True)),
                ('highlighted_review_is_anonymous', models.BooleanField(default=False, help_text='Highlighted review is anonymous')),
                ('highlighted_review_is_employee', models.BooleanField(default=False, help_text='Highlighted review is employee')),
                ('highlighted_review_product_id', models.IntegerField(blank=True, help_text='Highlighted review product ID', null=True)),
                ('highlighted_review_user_id', models.IntegerField(blank=True, help_text='Highlighted review user ID', null=True)),
                ('highlighted_review_is_hype', models.BooleanField(default=False, help_text='Highlighted review is hype')),
                ('is_fyndware', models.BooleanField(default=False, help_text='Is Fyndware')),
                ('is_fyndware_of', models.IntegerField(blank=True, help_text='The product ID of the real product', null=True)),
                ('fyndware_class', models.IntegerField(blank=True, help_text='Fyndware class', null=True)),
                ('main_title', models.TextField(blank=True, help_text='Main title')),
                ('sub_title', models.TextField(blank=True, help_text='Sub title')),
                ('is_shippable', models.BooleanField(default=False, help_text='Is shippable')),
                ('is_collectable', models.BooleanField(default=False, help_text='Is collectable')),
                ('excluded_shipping_methods', models.TextField(blank=True, help_text='Excluded shipping methods')),
                ('insurance_id', models.IntegerField(blank=True, help_text='Insurance ID', null=True)),
                ('possible_delivery_methods', models.TextField(blank=True, help_text='Possible delivery methods')),
            ],
        ),
        migrations.RenameModel(
            old_name='HistoricalWebhallen',
            new_name='HistoricalWebhallenJSON',
        ),
        migrations.RenameModel(
            old_name='Webhallen',
            new_name='WebhallenJSON',
        ),
        migrations.CreateModel(
            name='HistoricalWebhallenProduct',
            fields=[
                ('product_id', models.IntegerField(db_index=True, help_text='Product ID')),
                ('created', models.DateTimeField(blank=True, editable=False, help_text='Created')),
                ('updated', models.DateTimeField(blank=True, editable=False, help_text='Updated')),
                ('minimum_rank_level', models.IntegerField(blank=True, help_text='Minimum rank level', null=True)),
                ('images', models.TextField(blank=True, help_text='Comma separated image URLs')),
                ('name', models.TextField(blank=True, help_text='Product name')),
                ('price', models.TextField(blank=True, help_text='Product price')),
                ('vat', models.TextField(blank=True, help_text='Product VAT')),
                ('price_end_at', models.DateTimeField(blank=True, help_text='Price end at', null=True)),
                ('price_nearly_over', models.BooleanField(default=False, help_text='Price nearly over')),
                ('price_flash_sale', models.BooleanField(default=False, help_text='Price flash sale')),
                ('price_type', models.TextField(blank=True, help_text='Price type')),
                ('regular_price', models.TextField(blank=True, help_text='Regular price')),
                ('regular_price_type', models.TextField(blank=True, help_text='Regular price type')),
                ('regular_price_end_at', models.DateTimeField(blank=True, help_text='Regular price end at', null=True)),
                ('regular_price_nearly_over', models.BooleanField(default=False, help_text='Regular price nearly over')),
                ('regular_price_flash_sale', models.BooleanField(default=False, help_text='Regular price flash sale')),
                ('lowest_price', models.TextField(blank=True, help_text='Lowest price')),
                ('lowest_price_type', models.TextField(blank=True, help_text='Lowest price type')),
                ('lowest_price_end_at', models.DateTimeField(blank=True, help_text='Lowest price end at', null=True)),
                ('lowest_price_nearly_over', models.BooleanField(default=False, help_text='Lowest price nearly over')),
                ('lowest_price_flash_sale', models.BooleanField(default=False, help_text='Lowest price flash sale')),
                ('level_one_price', models.TextField(blank=True, help_text='Level one price')),
                ('level_one_price_type', models.TextField(blank=True, help_text='Level one price type')),
                ('level_one_price_end_at', models.DateTimeField(blank=True, help_text='Level one price end at', null=True)),
                ('level_one_price_nearly_over', models.BooleanField(default=False, help_text='Level one price nearly over')),
                ('level_one_price_flash_sale', models.BooleanField(default=False, help_text='Level one price flash sale')),
                ('description', models.TextField(blank=True, help_text='Product description')),
                ('meta_title', models.TextField(blank=True, help_text='Product meta title')),
                ('meta_description', models.TextField(blank=True, help_text='Product meta description')),
                ('canonical_url', models.TextField(blank=True, help_text='Product canonical URL')),
                ('release_date', models.DateTimeField(blank=True, help_text='Product release date', null=True)),
                ('section_id', models.IntegerField(blank=True, help_text='Section ID', null=True)),
                ('is_digital', models.BooleanField(default=False, help_text='Is digital')),
                ('discontinued', models.BooleanField(default=False, help_text='Discontinued')),
                ('category_tree', models.TextField(blank=True, help_text='Category tree')),
                ('main_category_path', models.TextField(blank=True, help_text='Comma separated main category path')),
                ('manufacturer', models.IntegerField(blank=True, help_text='Manufacturer', null=True)),
                ('part_numbers', models.TextField(blank=True, help_text='Comma separated list of part numbers')),
                ('eans', models.TextField(blank=True, help_text='Comma separated list of EANs')),
                ('thumbnail', models.TextField(blank=True, help_text='Thumbnail URL')),
                ('average_rating', models.FloatField(blank=True, help_text='Average rating', null=True)),
                ('average_rating_type', models.TextField(blank=True, help_text='Average rating type')),
                ('energy_marking', models.TextField(blank=True, help_text='Energy marking')),
                ('package_size_id', models.IntegerField(blank=True, help_text='Package size ID', null=True)),
                ('status_codes', models.TextField(blank=True, help_text='Comma separated list of status codes')),
                ('long_delivery_notice', models.TextField(blank=True, help_text='Long delivery notice')),
                ('categories', models.TextField(blank=True, help_text='Comma separated list of categories')),
                ('phone_subscription', models.BooleanField(default=False, help_text='Phone subscription')),
                ('highlighted_review_id', models.IntegerField(blank=True, help_text='Highlighted review ID', null=True)),
                ('highlighted_review_text', models.TextField(blank=True, help_text='Highlighted review text')),
                ('highlighted_review_rating', models.IntegerField(blank=True, help_text='Highlighted review rating', null=True)),
                ('highlighted_review_upvotes', models.IntegerField(blank=True, help_text='Highlighted review upvotes', null=True)),
                ('highlighted_review_downvotes', models.IntegerField(blank=True, help_text='Highlighted review downvotes', null=True)),
                ('highlighted_review_verified', models.BooleanField(default=False, help_text='Highlighted review verified')),
                ('highlighted_review_created', models.DateTimeField(blank=True, help_text='Highlighted review created', null=True)),
                ('highlighted_review_is_anonymous', models.BooleanField(default=False, help_text='Highlighted review is anonymous')),
                ('highlighted_review_is_employee', models.BooleanField(default=False, help_text='Highlighted review is employee')),
                ('highlighted_review_product_id', models.IntegerField(blank=True, help_text='Highlighted review product ID', null=True)),
                ('highlighted_review_user_id', models.IntegerField(blank=True, help_text='Highlighted review user ID', null=True)),
                ('highlighted_review_is_hype', models.BooleanField(default=False, help_text='Highlighted review is hype')),
                ('is_fyndware', models.BooleanField(default=False, help_text='Is Fyndware')),
                ('is_fyndware_of', models.IntegerField(blank=True, help_text='The product ID of the real product', null=True)),
                ('fyndware_class', models.IntegerField(blank=True, help_text='Fyndware class', null=True)),
                ('main_title', models.TextField(blank=True, help_text='Main title')),
                ('sub_title', models.TextField(blank=True, help_text='Sub title')),
                ('is_shippable', models.BooleanField(default=False, help_text='Is shippable')),
                ('is_collectable', models.BooleanField(default=False, help_text='Is collectable')),
                ('excluded_shipping_methods', models.TextField(blank=True, help_text='Excluded shipping methods')),
                ('insurance_id', models.IntegerField(blank=True, help_text='Insurance ID', null=True)),
                ('possible_delivery_methods', models.TextField(blank=True, help_text='Possible delivery methods')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical webhallen product',
                'verbose_name_plural': 'historical webhallen products',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
