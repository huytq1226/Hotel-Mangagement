from django.db import models
from login.models import Customer, RoomManager

# Model Contact lưu trữ thông tin liên hệ của khách hàng
class Contact(models.Model):
    name = models.CharField(max_length=100)      # Tên người liên hệ
    email = models.CharField(max_length=100)     # Email liên hệ
    message = models.TextField(max_length=2000)  # Nội dung tin nhắn
    def __str__(self):
        return self.name

# Model Rooms quản lý thông tin các phòng trong hệ thống
class Rooms(models.Model):
    manager = models.ForeignKey(RoomManager, on_delete=models.SET_NULL, null=True)  # Người quản lý phòng
    room_no = models.CharField(max_length=5)        # Số phòng
    room_type = models.CharField(max_length=50)     # Loại phòng
    is_available = models.BooleanField(default=True)  # Trạng thái phòng
    price = models.FloatField()                     # Giá phòng
    no_of_days_advance = models.IntegerField()      # Số ngày có thể đặt trước
    start_date = models.DateField(null=True)        # Ngày bắt đầu cho thuê
    room_image = models.ImageField(
        upload_to="media", 
        blank=True,
        null=True,
        default='media/default_room.jpg'
    )
    def __str__(self):
        return "Room No: "+str(self.room_no)

# Model Booking quản lý thông tin đặt phòng
class Booking(models.Model):
    room_no = models.ForeignKey(Rooms, on_delete=models.CASCADE)  # Phòng được đặt
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Người đặt
    start_day = models.DateField()        # Ngày bắt đầu
    end_day = models.DateField()          # Ngày kết thúc
    amount = models.FloatField()          # Tổng tiền
    booked_on = models.DateTimeField(auto_now=True)  # Thời điểm đặt phòng
    payment_status = models.CharField(max_length=15)  # Trạng thái thanh toán
    payment_method = models.CharField(max_length=15)  # Phương thức thanh toán
    def __str__(self):
        return "Booking ID: "+str(self.id)


