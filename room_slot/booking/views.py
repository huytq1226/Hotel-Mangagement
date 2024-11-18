from django.shortcuts import render,redirect
from .models import Contact
from .models import Rooms,Booking
from login.models import Customer
from django.contrib import messages
from django.http import HttpResponse
import datetime
from django.db.models import Q

def index(request):
    # Lấy tham số sắp xếp và tìm kiếm từ URL
    sort_by = request.GET.get('sort', 'room_type')
    order = request.GET.get('order', 'asc')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Lọc phòng trống
    rooms = Rooms.objects.filter(is_available=True)

    # Lọc theo khoảng giá nếu có
    if min_price:
        rooms = rooms.filter(price__gte=float(min_price))
    if max_price:
        rooms = rooms.filter(price__lte=float(max_price))

    # Xử lý sắp xếp
    if sort_by == 'price':
        if order == 'desc':
            rooms = rooms.order_by('-price')
        else:
            rooms = rooms.order_by('price')
    else:  # sort by room_type
        if order == 'desc':
            rooms = rooms.order_by('-room_type')
        else:
            rooms = rooms.order_by('room_type')

    context = {
        'rooms': rooms,
        'current_sort': sort_by,
        'current_order': order,
        'min_price': min_price or '',
        'max_price': max_price or ''
    }
    return render(request, 'booking/index.html', context)

def contact(request):
    if request.method=="GET":
     return render(request,"contact/contact.html",{})
    else:
     username=request.POST['name']
     email=request.POST['email']
     message=request.POST['message']
     data=Contact(name=username,email=email,message=message)
     data.save()
     return render(request,"contact/contact.html",{'message':'Thank you for contacting us.'})

def book(request):
    if request.method=="POST":
        start_date=request.POST['start_date']
        end_date=request.POST['end_date']
        request.session['start_date']=start_date
        request.session['end_date']=end_date
        start_date=datetime.datetime.strptime(start_date, "%d/%b/%Y").date()
        end_date=datetime.datetime.strptime(end_date, "%d/%b/%Y").date()
        no_of_days=(end_date-start_date).days
        
        # Thay đổi cách lấy dữ liệu, không dùng values()
        data = Rooms.objects.filter(
            is_available=True,
            no_of_days_advance__gte=no_of_days,
            start_date__lte=start_date
        )
        
        request.session['no_of_days']=no_of_days
        return render(request,'booking/book.html',{'data':data})
    else:
        return redirect('index')

def book_now(request, id):
    if request.session.get("username",None) and request.session.get("type",None)=='customer':
        if request.session.get("no_of_days",1):
            try:
                no_of_days = request.session['no_of_days']
                start_date = request.session['start_date']
                end_date = request.session['end_date']
                request.session['room_no'] = id
                
                data = Rooms.objects.get(id=id)
                
                bill = data.price * int(no_of_days)
                deposit = bill * 0.5  # 50% đặt cọc
                
                request.session['bill'] = bill
                request.session['deposit'] = deposit
                
                # Xử lý trường hợp manager không tồn tại
                try:
                    roomManager = data.manager.username
                except (Customer.DoesNotExist, AttributeError):
                    roomManager = "Not assigned"
                
                return render(request, "booking/book-now.html", {
                    "no_of_days": no_of_days,
                    "room_no": data.room_no,
                    "data": data,
                    "bill": bill,
                    "deposit": deposit,
                    "roomManager": roomManager,
                    "start": start_date,
                    "end": end_date
                })
            except Rooms.DoesNotExist:
                messages.error(request, "Phòng không tồn tại")
                return redirect("index")
        else:
            return redirect("index")
    else:
        next = "book-now/" + str(id)
        return redirect('user_login')

def book_confirm(request):
    if request.method == "POST":
        payment_method = request.POST.get('payment_method')
        
        room_no = request.session['room_no']
        start_date = request.session['start_date']
        end_date = request.session['end_date']
        username = request.session['username']
        user_id = Customer.objects.get(username=username)
        room = Rooms.objects.get(id=room_no)
        amount = request.session['bill']
        
        if payment_method == 'online':
            payment_gateway = request.POST.get('payment_gateway')
            deposit = request.session['deposit']
            
            # Xử lý thanh toán online tùy theo cổng thanh toán
            if payment_gateway == 'momo':
                # Tích hợp MoMo
                pass
            elif payment_gateway == 'vnpay':
                # Tích hợp VNPay
                pass
            elif payment_gateway == 'zalopay':
                # Tích hợp ZaloPay
                pass
        
        # Lưu thông tin đặt phòng
        booking = Booking(
            room_no=room,
            user_id=user_id,
            start_day=datetime.datetime.strptime(start_date, "%d/%b/%Y").date(),
            end_day=datetime.datetime.strptime(end_date, "%d/%b/%Y").date(),
            amount=amount,
            payment_method=payment_method,
            payment_status='pending' if payment_method == 'offline' else 'partial'
        )
        booking.save()
        
        room.is_available = False
        room.save()
        
        # Xóa session
        for key in ['start_date', 'end_date', 'bill', 'room_no', 'deposit']:
            if key in request.session:
                del request.session[key]
        
        messages.success(request, "Đặt phòng thành công!")
        return redirect('user_dashboard')
    
    return redirect('index')

def cancel_room(request,id):
    data=Booking.objects.get(id=id)
    room=data.room_no
    room.is_available=True
    room.save()
    data.delete()
    return HttpResponse("Booking Cancelled Successfully")

def delete_room(request,id):
    data=Rooms.objects.get(id=id)
    manager=data.manager.username
    if manager==request.session['username']:
        data.delete()
        return HttpResponse("You have deleted the room successfully")
    else:
        return HttpResponse("Invalid Request")


            



    
