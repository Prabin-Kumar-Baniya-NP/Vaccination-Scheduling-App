# Generated by Django 4.0.3 on 2022-03-24 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('medical_condition', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vaccine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='Vaccine Name')),
                ('description', models.TextField(max_length=1024, verbose_name='Description')),
                ('number_of_doses', models.IntegerField(default=1, verbose_name='Number of Doses')),
                ('interval', models.IntegerField(default=0, help_text='Provide interval in days', verbose_name='Interval')),
                ('storage_temperature', models.IntegerField(blank=True, help_text='Provide Temperature in Celcius', null=True, verbose_name='Storage Temperature')),
                ('minimum_age', models.IntegerField(default=0, verbose_name='Minimum Age')),
                ('ineligible_medical_condition', models.ManyToManyField(blank=True, to='medical_condition.medical_condition')),
            ],
        ),
    ]
