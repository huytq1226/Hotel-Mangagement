from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0006_auto_20241119_2148'),  # Thay bằng migration cuối cùng của bạn
    ]

    operations = [
        migrations.AddField(
            model_name='rooms',
            name='hotel_name',
            field=models.CharField(default='Unknown Hotel', max_length=100),
        ),
    ] 