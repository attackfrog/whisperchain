# Generated by Django 2.0.7 on 2018-08-06 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_chain_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='chain',
            name='code',
            field=models.CharField(default='', max_length=6),
            preserve_default=False,
        ),
    ]
