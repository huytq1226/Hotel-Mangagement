from rest_framework import viewsets
from login.models import Customer
from booking.models import Booking, Rooms
from . import serializers

# ViewSet cho Customer - xử lý các request liên quan đến Customer
class CustomerViewset(viewsets.ModelViewSet):
    # Lấy tất cả customers từ database
    queryset = Customer.objects.all()
    # Sử dụng UserSerializer để chuyển đổi data
    serializer_class = serializers.UserSerializer
    # Hỗ trợ các operations:
    # - list(): GET /api/customer/
    # - create(): POST /api/customer/
    # - retrieve(): GET /api/customer/{id}/
    # - update(): PUT /api/customer/{id}/
    # - destroy(): DELETE /api/customer/{id}/

# ViewSet cho Rooms - xử lý các request liên quan đến Rooms
class RoomsViewset(viewsets.ModelViewSet):
    # Lấy tất cả rooms từ database
    queryset = Rooms.objects.all()
    # Sử dụng RoomsSerializer để chuyển đổi data
    serializer_class = serializers.RoomsSerializer
    # Tương tự như CustomerViewset, hỗ trợ đầy đủ CRUD operations

# ViewSet cho Booking - xử lý các request liên quan đến Booking
class BookingViewset(viewsets.ModelViewSet):
    # Lấy tất cả bookings từ database
    queryset = Booking.objects.all()
    # Sử dụng BookingSerializer để chuyển đổi data
    serializer_class = serializers.BookingSerializer
    # Tương tự như trên, hỗ trợ đầy đủ CRUD operations