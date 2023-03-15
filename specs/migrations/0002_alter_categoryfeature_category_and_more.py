# Generated by Django 4.0.1 on 2022-02-02 18:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_banner_alter_cart_final_price_alter_cart_owner_and_more'),
        ('specs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoryfeature',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.category', verbose_name='Категорія'),
        ),
        migrations.AlterField(
            model_name='categoryfeature',
            name='feature_filter_name',
            field=models.CharField(max_length=50, verbose_name="Ім'я для фільтру"),
        ),
        migrations.AlterField(
            model_name='categoryfeature',
            name='feature_name',
            field=models.CharField(max_length=50, verbose_name="Ім'я ключа категорії"),
        ),
        migrations.AlterField(
            model_name='categoryfeature',
            name='unit',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Одиниця виміру'),
        ),
        migrations.AlterField(
            model_name='featurevalidator',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.category', verbose_name='Категорія'),
        ),
        migrations.AlterField(
            model_name='featurevalidator',
            name='valid_feature_value',
            field=models.CharField(max_length=100, verbose_name='Валідне значення'),
        ),
        migrations.AlterField(
            model_name='productfeatures',
            name='value',
            field=models.CharField(max_length=255, verbose_name='Значення'),
        ),
    ]