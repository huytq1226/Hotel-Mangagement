from django.urls import path
from . import views

# Định nghĩa các URL patterns cho ứng dụng booking
urlpatterns = [
    path('', views.index, name='index'),                    # Trang chủ hiển thị danh sách phòng
    path('contact-us', views.contact, name='contact'),      # Trang liên hệ
    path('book', views.book, name='book'),                  # Trang tìm kiếm phòng
    path('book-now/<int:id>', views.book_now, name='book_now'),  # Trang đặt phòng cụ thể
    path('book_confirm', views.book_confirm, name='book_confirm'),  # Xử lý xác nhận đặt phòng
    path('cancel-room/<int:id>', views.cancel_room, name='cancel_room'),  # Hủy đặt phòng
    path('delete_room/<int:id>', views.delete_room, name='delete_room'),  # Xóa phòng
]