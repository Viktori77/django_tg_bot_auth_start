# Generated by Django 5.1.3 on 2024-12-01 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='authtoken',
            name='user_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
