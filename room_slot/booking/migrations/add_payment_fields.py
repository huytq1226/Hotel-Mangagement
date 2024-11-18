from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),  # Thay bằng tên migration cuối cùng của bạn
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='payment_method',
            field=models.CharField(choices=[('online', 'Thanh toán online'), ('offline', 'Thanh toán tại khách sạn')], default='offline', max_length=10),
        ),
        migrations.AddField(
            model_name='booking',
            name='payment_status',
            field=models.CharField(choices=[('pending', 'Chưa thanh toán'), ('partial', 'Đã thanh toán một phần'), ('completed', 'Đã thanh toán đủ')], default='pending', max_length=10),
        ),
        migrations.AddField(
            model_name='booking',
            name='deposit_amount',
            field=models.FloatField(blank=True, null=True),
        ),
    ] 