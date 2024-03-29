# Generated by Django 4.0.5 on 2022-06-23 14:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("vaccine", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("center", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Campaign",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_date", models.DateField(null=True, verbose_name="Start Date")),
                ("end_date", models.DateField(null=True, verbose_name="End Date")),
                (
                    "agents",
                    models.ManyToManyField(
                        blank=True, to=settings.AUTH_USER_MODEL, verbose_name="Agents"
                    ),
                ),
                (
                    "center",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="center.center",
                        verbose_name="Center",
                    ),
                ),
                (
                    "vaccine",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="vaccine.vaccine",
                        verbose_name="Vaccine",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Slot",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField(null=True, verbose_name="Date")),
                ("start_time", models.TimeField(verbose_name="Start Time")),
                ("end_time", models.TimeField(verbose_name="End Time")),
                (
                    "max_capacity",
                    models.IntegerField(default=0, verbose_name="Maximum Capacity"),
                ),
                (
                    "reserved",
                    models.IntegerField(default=0, verbose_name="Total Reserved"),
                ),
                (
                    "campaign",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="vaccination.campaign",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Vaccination",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "is_vaccinated",
                    models.BooleanField(default=False, verbose_name="Is Vaccinated"),
                ),
                (
                    "updated_on",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="Updated On"
                    ),
                ),
                (
                    "campaign",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="vaccination.campaign",
                        verbose_name="Campaign",
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="patient",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Patient",
                    ),
                ),
                (
                    "slot",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="vaccination.slot",
                        verbose_name="Slot",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Updated By",
                    ),
                ),
            ],
        ),
    ]
