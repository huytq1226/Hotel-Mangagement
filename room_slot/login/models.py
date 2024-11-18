from django.db import models
from PIL import Image

class Customer(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    email=models.CharField(max_length=50)
    profile_pic=models.ImageField(upload_to="media", height_field=None, width_field=None, max_length=None,blank=True)
    phone_no=models.CharField(max_length=50)
    address=models.TextField()
    state=models.CharField(max_length=30,blank=True)
    pin_code=models.IntegerField(blank=True)
    def __str__(self):
        return "Customer: "+self.username

class RoomManager(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    email=models.CharField(max_length=50)
    profile_pic=models.ImageField(upload_to="media", height_field=None, width_field=None, max_length=None,blank=True)
    phone_no=models.CharField(max_length=50)
    gender=models.CharField(max_length=20)
    def __str__(self):
        return "Room Manager: "+self.username

class Revenue(models.Model):
    date = models.DateField()
    total_bookings = models.IntegerField()
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    profit = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = 'Revenue'
        verbose_name_plural = 'Revenues'

    def __str__(self):
        return f"Revenue for {self.date}"

class Room(models.Model):
    # ... existing fields ...
    rating = models.FloatField(default=0)  # Lưu điểm trung bình
    rating_count = models.IntegerField(default=0)  # Lưu số lượt đánh giá

