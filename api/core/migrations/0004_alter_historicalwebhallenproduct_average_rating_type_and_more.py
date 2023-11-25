# Generated by Django 4.2.7 on 2023-11-24 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_rename_is_fyndware_of_historicalwebhallenproduct_fyndware_of_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalwebhallenproduct',
            name='average_rating_type',
            field=models.TextField(blank=True, default='', help_text='Average rating type'),
        ),
        migrations.AlterField(
            model_name='historicalwebhallenproduct',
            name='canonical_url',
            field=models.TextField(blank=True, default='', help_text='Product canonical URL'),
        ),
        migrations.AlterField(
            model_name='historicalwebhallenproduct',
            name='categories',
            field=models.TextField(blank=True, default='', help_text='Comma separated list of categories'),
        ),
        migrations.AlterField(
            model_name='historicalwebhallenproduct',
            name='category_tree',
            field=models.TextField(blank=True, default='', help_text='Category tree'),
        ),
        migrations.AlterField(
            model_name='historicalwebhallenproduct',
            name='description',
            field=models.TextField(blank=True, default='', help_text='Product description'),
        ),
        migrations.AlterField(
            model_name='historicalwebhallenproduct',
            name='eans',
            field=models.TextField(blank=True, default='', help_text='Comma separated list of EANs'),
        ),
        migrations.AlterField(
            model_name='historicalwebhallenproduct',
            name='energy_marking_label',
            field=models.TextField(blank=True, default='', help_text='Energy rating label link'),
        ),
        migrations.AlterField(
            model_name='historicalwebhallenproduct',
            name='energy_marking_rating',
            field=models.TextField(blank=True, default='', help_text='Energy marking rating (F to A)'),
        ),
        migrations.AlterField(
            model_name='historicalwebhallenproduct',
            name='excluded_shipping_methods',
            field=models.TextField(blank=True, default='', help_text='Excluded shipping methods'),
        ),
        migrations.AlterField(
            model_name='historicalwebhallenproduct',
            name='fyndware_of_description',
            field=models.TextField(blank=True, default='', help_text='Fyndware of description'),
        ),
        migrations.AlterField(
            model_name='historicalwebhallenproduct',
            name='highlighted_review_text',
            field=models.TextField(blank=True, default='', help_text='Highlighted review text'),
        ),
        migrations.AlterField(
            model_name='historicalwebhallenproduct',
            name='images_large',
            field=models.TextField(blank=True, default='', help_text='Comma separated list of large images'),
        ),
        migrations.AlterField(
            model_name='historicalwebhallenproduct',
            name='images_thumb',
            field=models.TextField(blank=True, default='', help_text='Comma separated list of thumbnail images'),
        ),
        migrations.AlterField(
            model_name='historicalwebhallenproduct',
            name='images_zoom',
            field=models.TextField(blank=True, default='', help_text='Comma separated list of zoom images'),
        ),
        migrations.AlterField(
            model_name='historicalwebhallenproduct',
            name='level_one_price',
            field=models.TextField(blank=True, default='', help_text='Level one price'),
        ),
        migrations.AlterField(
            model_name='historicalwebhallenproduct',
            name='level_one_price_type',
            field=models.TextField(blank=True, default='', help_text='Level one price type'),
        ),
        migrations.AlterField(
            model_name='historicalwebhallenproduct',
            name='long_delivery_notice',
            field=models.TextField(blank=True, default='', help_text='Long delivery notice'),
        ),
        migrations.AlterField(
            model_name='historicalwebhallenproduct',
            name='lowest_price',
            field=models.TextField(blank=True, default='', help_text='Lowest price'),
        ),
        migrations.AlterField(
            model_name='historicalwebhallenproduct',
            name='lowest_price_type',
            field=models.TextField(blank=True, default='', help_text='Lowest price type'),
        ),
        migrations.AlterField(
            model_name='historicalwebhallenproduct',
            name='main_category_path',
            field=models.TextField(blank=True, default='', help_text='Comma separated main category path'),
        ),
        migrations.AlterField(
            model_name='historicalwebhallenproduct',
            name='main_title',
            field=models.TextField(blank=True, default='', help_text='Main title'),
        ),
        migrations.AlterField(
            model_name='historicalwebhallenproduct',
            name='meta_description',
            field=models.TextField(blank=True, default='', help_text='Product meta description'),
        ),
        migrations.AlterField(
            model_name='historicalwebhallenproduct',
            name='meta_title',
            field=models.TextField(blank=True, default='', help_text='Product meta title'),
        ),
        migrations.AlterField(
            model_name='historicalwebhallenproduct',
            name='name',
            field=models.TextField(blank=True, default='', help_text='Product name'),
        ),
        migrations.AlterField(
            model_name='historicalwebhallenproduct',
            name='part_numbers',
            field=models.TextField(blank=True, default='', help_text='Comma separated list of part numbers'),
        ),
        migrations.AlterField(
            model_name='historicalwebhallenproduct',
            name='possible_delivery_methods',
            field=models.TextField(blank=True, default='', help_text='Possible delivery methods'),
        ),
        migrations.AlterField(
            model_name='historicalwebhallenproduct',
            name='price',
            field=models.TextField(blank=True, default='', help_text='Product price'),
        ),
        migrations.AlterField(
            model_name='historicalwebhallenproduct',
            name='price_type',
            field=models.TextField(blank=True, default='', help_text='Price type'),
        ),
        migrations.AlterField(
            model_name='historicalwebhallenproduct',
            name='regular_price',
            field=models.TextField(blank=True, default='', help_text='Regular price'),
        ),
        migrations.AlterField(
            model_name='historicalwebhallenproduct',
            name='regular_price_type',
            field=models.TextField(blank=True, default='', help_text='Regular price type'),
        ),
        migrations.AlterField(
            model_name='historicalwebhallenproduct',
            name='release_date',
            field=models.TextField(blank=True, default='', help_text='Product release date'),
        ),
        migrations.AlterField(
            model_name='historicalwebhallenproduct',
            name='status_codes',
            field=models.TextField(blank=True, default='', help_text='Comma separated list of status codes'),
        ),
        migrations.AlterField(
            model_name='historicalwebhallenproduct',
            name='sub_title',
            field=models.TextField(blank=True, default='', help_text='Sub title'),
        ),
        migrations.AlterField(
            model_name='historicalwebhallenproduct',
            name='thumbnail',
            field=models.TextField(blank=True, default='', help_text='Thumbnail URL'),
        ),
        migrations.AlterField(
            model_name='historicalwebhallenproduct',
            name='vat',
            field=models.TextField(blank=True, default='', help_text='Product VAT'),
        ),
        migrations.AlterField(
            model_name='webhallenproduct',
            name='average_rating_type',
            field=models.TextField(blank=True, default='', help_text='Average rating type'),
        ),
        migrations.AlterField(
            model_name='webhallenproduct',
            name='canonical_url',
            field=models.TextField(blank=True, default='', help_text='Product canonical URL'),
        ),
        migrations.AlterField(
            model_name='webhallenproduct',
            name='categories',
            field=models.TextField(blank=True, default='', help_text='Comma separated list of categories'),
        ),
        migrations.AlterField(
            model_name='webhallenproduct',
            name='category_tree',
            field=models.TextField(blank=True, default='', help_text='Category tree'),
        ),
        migrations.AlterField(
            model_name='webhallenproduct',
            name='description',
            field=models.TextField(blank=True, default='', help_text='Product description'),
        ),
        migrations.AlterField(
            model_name='webhallenproduct',
            name='eans',
            field=models.TextField(blank=True, default='', help_text='Comma separated list of EANs'),
        ),
        migrations.AlterField(
            model_name='webhallenproduct',
            name='energy_marking_label',
            field=models.TextField(blank=True, default='', help_text='Energy rating label link'),
        ),
        migrations.AlterField(
            model_name='webhallenproduct',
            name='energy_marking_rating',
            field=models.TextField(blank=True, default='', help_text='Energy marking rating (F to A)'),
        ),
        migrations.AlterField(
            model_name='webhallenproduct',
            name='excluded_shipping_methods',
            field=models.TextField(blank=True, default='', help_text='Excluded shipping methods'),
        ),
        migrations.AlterField(
            model_name='webhallenproduct',
            name='fyndware_of_description',
            field=models.TextField(blank=True, default='', help_text='Fyndware of description'),
        ),
        migrations.AlterField(
            model_name='webhallenproduct',
            name='highlighted_review_text',
            field=models.TextField(blank=True, default='', help_text='Highlighted review text'),
        ),
        migrations.AlterField(
            model_name='webhallenproduct',
            name='images_large',
            field=models.TextField(blank=True, default='', help_text='Comma separated list of large images'),
        ),
        migrations.AlterField(
            model_name='webhallenproduct',
            name='images_thumb',
            field=models.TextField(blank=True, default='', help_text='Comma separated list of thumbnail images'),
        ),
        migrations.AlterField(
            model_name='webhallenproduct',
            name='images_zoom',
            field=models.TextField(blank=True, default='', help_text='Comma separated list of zoom images'),
        ),
        migrations.AlterField(
            model_name='webhallenproduct',
            name='level_one_price',
            field=models.TextField(blank=True, default='', help_text='Level one price'),
        ),
        migrations.AlterField(
            model_name='webhallenproduct',
            name='level_one_price_type',
            field=models.TextField(blank=True, default='', help_text='Level one price type'),
        ),
        migrations.AlterField(
            model_name='webhallenproduct',
            name='long_delivery_notice',
            field=models.TextField(blank=True, default='', help_text='Long delivery notice'),
        ),
        migrations.AlterField(
            model_name='webhallenproduct',
            name='lowest_price',
            field=models.TextField(blank=True, default='', help_text='Lowest price'),
        ),
        migrations.AlterField(
            model_name='webhallenproduct',
            name='lowest_price_type',
            field=models.TextField(blank=True, default='', help_text='Lowest price type'),
        ),
        migrations.AlterField(
            model_name='webhallenproduct',
            name='main_category_path',
            field=models.TextField(blank=True, default='', help_text='Comma separated main category path'),
        ),
        migrations.AlterField(
            model_name='webhallenproduct',
            name='main_title',
            field=models.TextField(blank=True, default='', help_text='Main title'),
        ),
        migrations.AlterField(
            model_name='webhallenproduct',
            name='meta_description',
            field=models.TextField(blank=True, default='', help_text='Product meta description'),
        ),
        migrations.AlterField(
            model_name='webhallenproduct',
            name='meta_title',
            field=models.TextField(blank=True, default='', help_text='Product meta title'),
        ),
        migrations.AlterField(
            model_name='webhallenproduct',
            name='name',
            field=models.TextField(blank=True, default='', help_text='Product name'),
        ),
        migrations.AlterField(
            model_name='webhallenproduct',
            name='part_numbers',
            field=models.TextField(blank=True, default='', help_text='Comma separated list of part numbers'),
        ),
        migrations.AlterField(
            model_name='webhallenproduct',
            name='possible_delivery_methods',
            field=models.TextField(blank=True, default='', help_text='Possible delivery methods'),
        ),
        migrations.AlterField(
            model_name='webhallenproduct',
            name='price',
            field=models.TextField(blank=True, default='', help_text='Product price'),
        ),
        migrations.AlterField(
            model_name='webhallenproduct',
            name='price_type',
            field=models.TextField(blank=True, default='', help_text='Price type'),
        ),
        migrations.AlterField(
            model_name='webhallenproduct',
            name='regular_price',
            field=models.TextField(blank=True, default='', help_text='Regular price'),
        ),
        migrations.AlterField(
            model_name='webhallenproduct',
            name='regular_price_type',
            field=models.TextField(blank=True, default='', help_text='Regular price type'),
        ),
        migrations.AlterField(
            model_name='webhallenproduct',
            name='release_date',
            field=models.TextField(blank=True, default='', help_text='Product release date'),
        ),
        migrations.AlterField(
            model_name='webhallenproduct',
            name='status_codes',
            field=models.TextField(blank=True, default='', help_text='Comma separated list of status codes'),
        ),
        migrations.AlterField(
            model_name='webhallenproduct',
            name='sub_title',
            field=models.TextField(blank=True, default='', help_text='Sub title'),
        ),
        migrations.AlterField(
            model_name='webhallenproduct',
            name='thumbnail',
            field=models.TextField(blank=True, default='', help_text='Thumbnail URL'),
        ),
        migrations.AlterField(
            model_name='webhallenproduct',
            name='vat',
            field=models.TextField(blank=True, default='', help_text='Product VAT'),
        ),
    ]