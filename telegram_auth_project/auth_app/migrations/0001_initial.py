# Generated by Django 5.1.3 on 2024-12-01 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=64, unique=True)),
                ('session_key', models.CharField(max_length=64)),
                ('is_authenticated', models.BooleanField(default=False)),
            ],
        ),
    ]
