from django.shortcuts import render,redirect
from login.models import Customer
from booking.models import Booking
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.contrib.auth.hashers import make_password



import datetime
def dashboard(request):
  if request.session.get('username',None) and request.session.get('type',None)=='manager':
        return redirect('manager_dashboard')
  if request.session.get('username',None) and request.session.get('type',None)=='customer':
      username=request.session['username']
      data=Customer.objects.get(username=username)
      booking_data=Booking.objects.filter(user_id=data).order_by('-id')
      counts=booking_data.filter(end_day__lt=datetime.datetime.now()).count()
      available=len(booking_data)-counts
      return render(request,"user_dash/index.html",{"data":booking_data,"count":counts,"available":available})
  else:
      return redirect("user_login")
  
def details(request,id,booking_id):
    if not request.session.get('username',None):
      return redirect('manager_login')
    if request.session.get('username',None) and request.session.get('type',None)=='customer':
        return redirect('user_dashboard')
    try:
        booking_data=Booking.objects.get(id=booking_id)
        user=Customer.objects.get(id=id)
        return render(request,"user_dash/details.html",{"user":user,"booking_data":booking_data})
    except:
        return redirect("/manager/dashboard1/")


def change_password(request):
    if not request.session.get('username', None):
        return redirect('user_login')

    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        username = request.session['username']
        user = Customer.objects.get(username=username)

        # Kiểm tra mật khẩu cũ
        if not check_password(old_password, user.password):  # Nếu bạn dùng hash
            messages.error(request, 'Mật khẩu cũ không chính xác.')
            return redirect('change_password')

        # Kiểm tra mật khẩu mới và xác nhận
        if new_password != confirm_password:
            messages.error(request, 'Mật khẩu mới và xác nhận mật khẩu không khớp.')
            return redirect('change_password')

        # Cập nhật mật khẩu mới
        user.password = make_password(new_password)  # Dùng hash mật khẩu
        user.save()

        messages.success(request, 'Đổi mật khẩu thành công.')
        return redirect('user_dashboard')

    return render(request, 'user_dash/change_password.html')
