# Generated by Django 5.0.8 on 2024-11-14 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0002_alter_billing_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='profile_pic',
            field=models.FileField(blank=True, null=True, upload_to='doctor_profile/'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='profile_pic',
            field=models.FileField(blank=True, null=True, upload_to='patient_profile/'),
        ),
    ]
