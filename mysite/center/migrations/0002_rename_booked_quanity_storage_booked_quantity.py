# Generated by Django 4.0.2 on 2022-03-11 06:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('center', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='storage',
            old_name='booked_quanity',
            new_name='booked_quantity',
        ),
    ]
