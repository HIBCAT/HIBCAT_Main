# Generated by Django 3.1.5 on 2021-01-17 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ibhi', '0002_auto_20210117_0135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinecenter',
            name='publication_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]