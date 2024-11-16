# Generated by Django 4.2.5 on 2024-11-16 11:35

from django.db import migrations, models
import shortener.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='URL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_url', models.URLField(max_length=2048)),
                ('short_code', models.CharField(default=shortener.models.generate_short_code, max_length=10, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
