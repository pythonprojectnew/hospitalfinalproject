# Generated by Django 5.1.3 on 2024-11-27 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0003_alter_doctor_profile_pic_alter_patient_profile_pic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='is_approved',
        ),
    ]
