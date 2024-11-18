import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'room_slot.settings')
django.setup()

from booking.models import Rooms

def update_existing_rooms():
    rooms = Rooms.objects.all()
    for room in rooms:
        if room.rating is None:  # Chỉ cập nhật các phòng chưa có rating
            room.rating = round(random.uniform(4.0, 5.0), 1)
            room.rating_count = random.randint(10, 50)
            room.save()
            print(f'Updated room {room.room_no}: {room.rating} stars ({room.rating_count} ratings)')

if __name__ == '__main__':
    update_existing_rooms() 