# Generated by Django 3.2.7 on 2021-12-21 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Services', '0011_alter_services_serv_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='services',
            name='Serv_Location',
            field=models.CharField(blank=True, default=None, max_length=300, null=True),
        ),
    ]
