default_app_config = 'booking.apps.BookingConfig'

# Định nghĩa các hằng số cho app
PAYMENT_STATUS_CHOICES = (
    ('pending', 'Chờ thanh toán'),
    ('partial', 'Đã đặt cọc'),
    ('completed', 'Đã thanh toán'),
    ('cancelled', 'Đã hủy')
)

PAYMENT_METHOD_CHOICES = (
    ('online', 'Thanh toán online'),
    ('offline', 'Thanh toán tại khách sạn')
)
