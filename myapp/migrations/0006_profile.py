# Generated by Django 4.0.2 on 2023-06-05 11:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0005_bid_winner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField(blank=True, max_length=50)),
                ('about', models.TextField(blank=True)),
                ('fb', models.URLField(blank=True)),
                ('linkedIn', models.URLField(blank=True)),
                ('ins', models.URLField(blank=True)),
                ('google', models.URLField(blank=True)),
                ('image', models.ImageField(upload_to='profile_images')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]