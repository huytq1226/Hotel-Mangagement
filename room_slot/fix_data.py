import os
import django

# Sửa đường dẫn settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'room_slot.settings')
django.setup()

from booking.models import Rooms
from login.models import Customer

def fix_rooms_data():
    # Lấy Customer đầu tiên làm manager mặc định
    default_manager = Customer.objects.first()
    if not default_manager:
        print("Không có Customer nào trong database. Hãy tạo một Customer trước.")
        return

    # Cập nhật tất cả các phòng có manager không hợp lệ
    invalid_rooms = Rooms.objects.filter(manager__isnull=True)
    for room in invalid_rooms:
        room.manager = default_manager
        room.save()
    
    print(f"Đã sửa {invalid_rooms.count()} phòng")

if __name__ == '__main__':
    fix_rooms_data() 