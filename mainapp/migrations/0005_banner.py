# Generated by Django 4.0.1 on 2022-02-04 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_delete_banner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Назва банера')),
                ('slug', models.SlugField(unique=True)),
                ('link', models.CharField(blank=True, max_length=255, null=True, verbose_name="Посилання (Не обов'язково)")),
                ('image', models.ImageField(upload_to='', verbose_name='Зображення')),
            ],
        ),
    ]