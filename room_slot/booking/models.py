from django.db import models
from login.models import Customer

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    message = models.TextField(max_length=2000)
    def __str__(self):
        return self.name

class Rooms(models.Model):
    manager = models.ForeignKey(Customer, on_delete=models.CASCADE)
    room_no = models.CharField(max_length=5)
    room_type = models.CharField(max_length=50)
    is_available = models.BooleanField(default=True)
    price = models.FloatField()
    no_of_days_advance = models.IntegerField()
    start_date = models.DateField()
    room_image = models.ImageField(upload_to="media", blank=True)
    def __str__(self):
        return "Room No: "+str(self.room_no)

class Booking(models.Model):
    room_no = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    start_day = models.DateField()
    end_day = models.DateField()
    amount = models.FloatField()
    booked_on = models.DateTimeField(auto_now=True)
    payment_status = models.CharField(max_length=15)
    payment_method = models.CharField(max_length=15)
    def __str__(self):
        return "Booking ID: "+str(self.id)


