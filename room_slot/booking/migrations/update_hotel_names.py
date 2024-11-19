from django.db import migrations

def update_hotel_names(apps, schema_editor):
    Rooms = apps.get_model('booking', 'Rooms')
    # Cập nhật tên khách sạn cho từng phòng
    for room in Rooms.objects.all():
        # Ví dụ: đặt tên khách sạn dựa trên room_type
        room.hotel_name = f"{room.room_type} Hotel"
        room.save()

class Migration(migrations.Migration):
    dependencies = [
        ('booking', 'add_hotel_name'),  # Phụ thuộc vào migration thêm trường hotel_name
    ]

    operations = [
        migrations.RunPython(update_hotel_names),
    ] 