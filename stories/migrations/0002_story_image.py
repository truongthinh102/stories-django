# Generated by Django 4.0 on 2022-09-15 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='image',
            field=models.ImageField(default='stories/images/logo.png', upload_to='stories/images'),
        ),
    ]
