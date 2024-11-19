default_app_config = 'login.apps.LoginConfig'

# Định nghĩa các hằng số cho app
USER_TYPE_CHOICES = (
    ('customer', 'Khách hàng'),
    ('manager', 'Quản lý phòng')
)

# Các thông báo lỗi
LOGIN_ERROR_MESSAGES = {
    'invalid_credentials': 'Tên đăng nhập hoặc mật khẩu không đúng',
    'account_disabled': 'Tài khoản đã bị vô hiệu hóa',
    'account_not_found': 'Không tìm thấy tài khoản'
}
