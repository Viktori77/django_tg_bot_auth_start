# Generated by Django 5.1.3 on 2024-12-01 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0002_authtoken_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='authtoken',
            name='username',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
