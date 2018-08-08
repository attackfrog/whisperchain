# Generated by Django 2.0.7 on 2018-08-08 20:04

from django.db import migrations, models
import web.helpers


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_auto_20180807_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='data',
            field=models.ImageField(height_field='height', upload_to=web.helpers.imagePath, width_field='width'),
        ),
        migrations.AlterField(
            model_name='picture',
            name='height',
            field=models.PositiveIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='picture',
            name='width',
            field=models.PositiveIntegerField(blank=True),
        ),
    ]
