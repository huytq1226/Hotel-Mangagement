import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'room_slot.settings')
django.setup()

from booking.models import Rooms
from login.models import Customer
from django.db import connection

def fix_manager_references():
    # Lấy danh sách các manager_id hiện có trong bảng Rooms
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT manager_id FROM booking_rooms WHERE manager_id IS NOT NULL")
        manager_ids = [row[0] for row in cursor.fetchall()]
    
    print(f"Found manager IDs in Rooms: {manager_ids}")
    
    # Lấy Customer đầu tiên hoặc tạo mới nếu không có
    default_manager = Customer.objects.first()
    if not default_manager:
        default_manager = Customer.objects.create(
            username='default_manager',
            password='manager123',
            email='manager@example.com',
            phone='1234567890',
            type='manager'
        )
        print(f"Created new default manager with ID: {default_manager.id}")
    else:
        print(f"Using existing manager with ID: {default_manager.id}")
    
    # Cập nhật trực tiếp trong database
    with connection.cursor() as cursor:
        # Cập nhật các phòng có manager_id không hợp lệ
        cursor.execute("""
            UPDATE booking_rooms 
            SET manager_id = %s 
            WHERE manager_id NOT IN (
                SELECT id FROM login_customer
            )
        """, [default_manager.id])
        
        rows_updated = cursor.rowcount
        print(f"Updated {rows_updated} rooms with invalid manager references")

if __name__ == '__main__':
    fix_manager_references() 