#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    # Thiết lập biến môi trường DJANGO_SETTINGS_MODULE
    # Chỉ định file settings.py mà Django sẽ sử dụng
    # 'room_slot.settings' nghĩa là file settings.py nằm trong thư mục room_slot/
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'room_slot.settings')
    
    try:
        # Import hàm execute_from_command_line từ django.core.management
        # Hàm này sẽ xử lý các command line arguments như:
        # - runserver: Khởi động development server
        # - makemigrations: Tạo các file migrations
        # - migrate: Áp dụng migrations vào database
        # - createsuperuser: Tạo tài khoản admin
        # - shell: Mở Django shell
        # - test: Chạy unit tests
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Nếu không import được Django, hiển thị thông báo lỗi
        # Nguyên nhân có thể do:
        # - Django chưa được cài đặt
        # - PYTHONPATH không đúng
        # - Virtual environment chưa được kích hoạt
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Thực thi command từ command line
    # sys.argv chứa các arguments được truyền vào khi chạy script
    # Ví dụ: python manage.py runserver 8000
    # sys.argv = ['manage.py', 'runserver', '8000']
    execute_from_command_line(sys.argv)


# Kiểm tra xem script có được chạy trực tiếp không
# Nếu file được import thì __name__ sẽ là tên module
# Nếu file được chạy trực tiếp thì __name__ sẽ là '__main__'
if __name__ == '__main__':
    # Gọi hàm main() khi script được chạy trực tiếp
    main()
