# Generated by Django 4.0.2 on 2022-03-11 06:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('center', '0002_rename_booked_quanity_storage_booked_quantity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='storage',
            old_name='available_quantity',
            new_name='total_quantity',
        ),
    ]
