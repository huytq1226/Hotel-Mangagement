from django.urls import path, include
from rest_framework import routers
from . import views

# Tạo router để tự động tạo các URL cho API
router = routers.DefaultRouter()

# Đăng ký các viewsets với router
# URL pattern sẽ là:
# GET /api/customer/ - Lấy danh sách customers
# POST /api/customer/ - Tạo customer mới
# GET /api/customer/{id}/ - Lấy thông tin một customer
# PUT /api/customer/{id}/ - Cập nhật thông tin customer
# DELETE /api/customer/{id}/ - Xóa customer
router.register(r'customer', views.CustomerViewset)
router.register(r'booking', views.BookingViewset)
router.register(r'rooms', views.RoomsViewset)

urlpatterns = [
    # Include tất cả URLs từ router
    path('', include(router.urls))
]
