# Generated by Django 3.0.3 on 2024-11-18 08:48
# Migration này thêm model Rating để quản lý đánh giá phòng

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0006_room'),
        ('booking', 'add_payment_fields'),
    ]

    operations = [
        # Tạo model Rating để lưu trữ đánh giá của khách hàng cho phòng
        migrations.CreateModel(
            name='Rating',
            fields=[
                # ID tự động tăng
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                # Điểm đánh giá từ 1-5 sao
                ('rating', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                # Thời gian đánh giá
                ('created_at', models.DateTimeField(auto_now_add=True)),
                # Liên kết với phòng được đánh giá
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='booking.Rooms')),
                # Liên kết với người đánh giá
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.Customer')),
            ],
            # Đảm bảo mỗi user chỉ đánh giá 1 phòng 1 lần
            options={
                'unique_together': {('room', 'user')},
            },
        ),
    ]
