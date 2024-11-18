import os
import django
import random

# Thiết lập môi trường Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'room_slot.settings')
django.setup()

from booking.models import Rooms, Rating
from login.models import Customer

def add_sample_ratings():
    rooms = Rooms.objects.all()
    customers = Customer.objects.all()

    if not customers:
        print("Không có khách hàng trong database!")
        return

    for room in rooms:
        # Xóa ratings cũ nếu có
        Rating.objects.filter(room=room).delete()
        
        # Tạo 5-10 đánh giá cho mỗi phòng
        num_ratings = random.randint(5, 10)
        
        # Lấy ngẫu nhiên các khách hàng
        selected_customers = random.sample(list(customers), min(num_ratings, len(customers)))
        
        for customer in selected_customers:
            # Tạo rating từ 3-5 sao
            rating_value = random.randint(3, 5)
            
            Rating.objects.create(
                room=room,
                user=customer,
                rating=rating_value
            )
        
        # In thông tin
        avg_rating = Rating.objects.filter(room=room).aggregate(django.db.models.Avg('rating'))['rating__avg']
        print(f'Phòng {room.room_no}: {num_ratings} đánh giá, trung bình {avg_rating:.1f} sao')

if __name__ == '__main__':
    add_sample_ratings() 