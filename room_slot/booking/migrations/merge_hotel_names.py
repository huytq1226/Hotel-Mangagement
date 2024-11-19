from django.db import migrations

def update_hotel_names(apps, schema_editor):
    Rooms = apps.get_model('booking', 'Rooms')
    
    # Danh sách các khách sạn nổi tiếng ở Việt Nam theo loại phòng
    hotel_types = {
        'Single Bed room': 'Sofitel Legend Metropole Hanoi',
        'Double Bed room': 'Rex Hotel Saigon',
        'Super Deluxe': 'Park Hyatt Saigon',
        'Beach Front Villa': 'Vinpearl Resort & Golf Nam Hoi An',
        'Classic Resort View': 'InterContinental Danang Sun Peninsula Resort',
        'Mountain Pool Villa': 'JW Marriott Phu Quoc Emerald Bay Resort',
        'Deluxe': 'The Reverie Saigon',
        'Suite': 'Azerai La Residence Hue',
        'Family': 'Melia Vinpearl Nha Trang Empire',
        'Standard': 'Caravelle Saigon Hotel',
        'Villa': 'Six Senses Ninh Van Bay',
        'Luxury': 'Banyan Tree Lang Co',
        'Premium': 'Anantara Quy Nhon Villas',
        'Presidential': 'Amanoi Resort Ninh Thuan',
        'Garden View': 'Four Seasons Resort The Nam Hai',
    }

    # Cập nhật tên khách sạn cho từng phòng
    for room in Rooms.objects.all():
        if room.room_type in hotel_types:
            room.hotel_name = hotel_types[room.room_type]
        else:
            # Nếu không tìm thấy mapping, sử dụng tên mặc định
            room.hotel_name = 'Khách sạn Hoàng Gia Việt Nam'
        room.save()

class Migration(migrations.Migration):
    dependencies = [
        ('booking', 'add_hotel_name'),
    ]

    operations = [
        migrations.RunPython(update_hotel_names),
    ] 