# Generated by Django 4.1.2 on 2023-01-19 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vaccination", "0003_vaccination_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vaccination",
            name="date",
            field=models.DateField(
                blank=True, null=True, verbose_name="Date of Vaccination"
            ),
        ),
    ]
