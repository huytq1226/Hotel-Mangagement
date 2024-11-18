from django.core.management.base import BaseCommand
from booking.models import Rooms, Rating
from login.models import Customer
import random

class Command(BaseCommand):
    help = 'Adds sample ratings to rooms'

    def handle(self, *args, **kwargs):
        rooms = Rooms.objects.all()
        customers = Customer.objects.all()

        if not customers.exists():
            self.stdout.write(self.style.ERROR('No customers found. Please create some customers first.'))
            return

        for room in rooms:
            # Tạo 3-7 đánh giá ngẫu nhiên cho mỗi phòng
            num_ratings = random.randint(3, 7)
            
            # Lấy ngẫu nhiên các khách hàng để đánh giá
            random_customers = random.sample(list(customers), min(num_ratings, len(customers)))
            
            for customer in random_customers:
                # Tạo rating ngẫu nhiên từ 3-5 sao (để điểm đánh giá thiên về tích cực)
                rating_value = random.randint(3, 5)
                
                Rating.objects.create(
                    room=room,
                    user=customer,
                    rating=rating_value
                )
            
            self.stdout.write(
                self.style.SUCCESS(f'Added {num_ratings} ratings to room {room.room_no}')
            ) 