# Generated by Django 4.2.5 on 2024-11-25 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensoracquisition',
            name='sensor_acquisitions',
            field=models.TextField(),
        ),
    ]