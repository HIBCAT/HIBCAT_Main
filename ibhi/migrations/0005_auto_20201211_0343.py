# Generated by Django 3.0.3 on 2020-12-11 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ibhi', '0004_auto_20201211_0335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinecenter',
            name='url',
            field=models.TextField(blank=True, null=True),
        ),
    ]
