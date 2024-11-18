from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('message', models.TextField(max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='Rooms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_no', models.CharField(max_length=10)),
                ('hotel_name', models.CharField(default='Unknown Hotel', max_length=100)),
                ('room_type', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('is_available', models.BooleanField(default=True)),
                ('room_image', models.ImageField(blank=True, null=True, upload_to='room_images/')),
                ('no_of_days_advance', models.IntegerField()),
                ('start_date', models.DateField(blank=True, null=True)),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.RoomManager')),
            ],
            options={
                'verbose_name': 'Room',
                'verbose_name_plural': 'Rooms',
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_day', models.DateField()),
                ('end_day', models.DateField()),
                ('amount', models.FloatField()),
                ('booked_on', models.DateTimeField(auto_now=True)),
                ('payment_method', models.CharField(choices=[('online', 'Thanh toán online'), ('offline', 'Thanh toán tại khách sạn')], default='offline', max_length=10)),
                ('payment_status', models.CharField(choices=[('pending', 'Chưa thanh toán'), ('partial', 'Đã thanh toán một phần'), ('completed', 'Đã thanh toán đủ')], default='pending', max_length=10)),
                ('deposit_amount', models.FloatField(blank=True, null=True)),
                ('room_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.Rooms')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.Customer')),
            ],
        ),
    ] 