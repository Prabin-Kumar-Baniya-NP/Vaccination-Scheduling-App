# Generated by Django 4.0.2 on 2022-03-08 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vaccine', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Center',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=124, verbose_name='Vaccination Center Name')),
                ('address', models.TextField(max_length=500, verbose_name='Address')),
                ('agents', models.ManyToManyField(blank=True, to='user.Agent')),
            ],
        ),
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available_quantity', models.IntegerField(default=0)),
                ('booked_quanity', models.IntegerField(default=0)),
                ('center', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='center.center')),
                ('vaccine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vaccine.vaccine')),
            ],
        ),
    ]
