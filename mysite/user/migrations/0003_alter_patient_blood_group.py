# Generated by Django 4.0 on 2022-04-03 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_agent_user_alter_patient_medical_record_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='blood_group',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
    ]
