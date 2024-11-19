from rest_framework import serializers
from login.models import Customer
from booking.models import Booking, Rooms

# Serializer cho model Customer - chuyển đổi thông tin user thành JSON
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        # Các trường sẽ được chuyển thành JSON
        fields = [
            'id',          # ID của user
            'username',    # Tên đăng nhập
            'password',    # Mật khẩu
            'email',       # Email
            'state',       # Tỉnh/thành phố
            'pin_code',    # Mã bưu điện
            'address',     # Địa chỉ
            'profile_pic'  # Ảnh đại diện
        ]

# Serializer cho model Rooms - chuyển đổi thông tin phòng thành JSON
class RoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        # Các trường sẽ được chuyển thành JSON
        fields = [
            'id',                  # ID của phòng
            'manager',             # Người quản lý phòng
            'room_no',             # Số phòng
            'room_type',           # Loại phòng
            'is_available',        # Trạng thái phòng (còn trống/đã đặt)
            'price',               # Giá phòng
            'no_of_days_advance',  # Số ngày có thể đặt trước
            'start_date',          # Ngày bắt đầu cho thuê
            'room_image'           # Ảnh phòng
        ]

# Serializer cho model Booking - chuyển đổi thông tin đặt phòng thành JSON
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        # Các trường sẽ được chuyển thành JSON
        fields = [
            'id',          # ID của booking
            'room_no',     # Phòng được đặt
            'user_id',     # Người đặt phòng
            'start_day',   # Ngày nhận phòng
            'end_day',     # Ngày trả phòng
            'amount',      # Tổng tiền
            'booked_on'    # Ngày đặt phòng
        ]