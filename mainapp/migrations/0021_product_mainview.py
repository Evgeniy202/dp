# Generated by Django 4.0.1 on 2022-03-31 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0020_remove_product_comment_delete_commentmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='mainView',
            field=models.BooleanField(default=True, verbose_name='Показувати на головній'),
        ),
    ]