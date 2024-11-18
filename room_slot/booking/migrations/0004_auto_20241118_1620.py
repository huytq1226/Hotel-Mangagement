# Generated by Django 3.0.3 on 2024-11-18 09:20

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0006_room'),
        ('booking', '0003_auto_20241118_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rooms',
            name='manager',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='login.Customer'),
        ),
        migrations.AlterField(
            model_name='rooms',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now, null=True),
        ),
    ]