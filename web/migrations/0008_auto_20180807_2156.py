# Generated by Django 2.0.7 on 2018-08-08 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_auto_20180806_2154'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='height',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='picture',
            name='width',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='chain',
            name='isPublic',
            field=models.BooleanField(verbose_name='Make Chain Public'),
        ),
        migrations.AlterField(
            model_name='chain',
            name='length',
            field=models.IntegerField(default=2),
        ),
        migrations.AlterField(
            model_name='chain',
            name='maxUsers',
            field=models.IntegerField(verbose_name='Maximum Users in Chain'),
        ),
        migrations.AlterField(
            model_name='picture',
            name='data',
            field=models.ImageField(height_field='height', upload_to='images/%Y/%m', width_field='width'),
        ),
    ]
