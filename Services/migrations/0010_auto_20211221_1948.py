# Generated by Django 3.2.7 on 2021-12-21 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Services', '0009_auto_20211220_2151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='services',
            name='Serv_Comp_Image',
            field=models.ImageField(blank=True, default='default_image.png', upload_to='Serv_Comp_pics/'),
        ),
        migrations.AlterField(
            model_name='services',
            name='Serv_Req_Image',
            field=models.ImageField(default='default_image.png', upload_to='Serv_Comp_pics/'),
        ),
    ]
