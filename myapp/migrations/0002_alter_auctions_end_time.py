# Generated by Django 4.0.2 on 2023-06-03 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctions',
            name='end_time',
            field=models.DateTimeField(blank=True),
        ),
    ]
