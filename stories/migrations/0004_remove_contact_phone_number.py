# Generated by Django 4.0 on 2022-09-28 16:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0003_contact'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='phone_number',
        ),
    ]