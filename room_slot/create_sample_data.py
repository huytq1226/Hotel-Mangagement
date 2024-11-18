import os
import django
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'room_slot.settings')
django.setup()

from login.models import Customer
from booking.models import Rooms

def create_sample_data():
    # Tạo một manager
    manager, created = Customer.objects.get_or_create(
        username='manager1',
        defaults={
            'password': 'manager123',
            'email': 'manager@example.com',
            'phone': '1234567890',
            'type': 'manager'
        }
    )

    # Tạo các phòng mẫu
    room_types = ['Standard', 'Deluxe', 'Super Deluxe', 'Suite']
    
    for i in range(1, 6):  # Tạo 5 phòng
        room = Rooms.objects.create(
            manager=manager,
            room_no=f'R{i:03d}',
            room_type=random.choice(room_types),
            is_available=True,
            price=random.randint(500000, 2000000),
            no_of_days_advance=30,
            start_date=datetime.now().date(),
            rating=round(random.uniform(4.0, 5.0), 1),
            rating_count=random.randint(10, 50)
        )
        print(f'Created room {room.room_no}')

if __name__ == '__main__':
    create_sample_data() 