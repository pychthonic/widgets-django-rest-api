# Generated by Django 4.1.2 on 2022-10-07 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('widgets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='widget',
            name='author_username',
            field=models.CharField(default='backend_dev', max_length=32),
        ),
    ]
