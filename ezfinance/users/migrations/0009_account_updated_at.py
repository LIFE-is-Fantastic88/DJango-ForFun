# Generated by Django 2.2.5 on 2020-02-24 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20200223_1300'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
