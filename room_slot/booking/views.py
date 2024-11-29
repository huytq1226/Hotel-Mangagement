from django.shortcuts import render,redirect
from .models import Contact
from .models import Rooms,Booking
from login.models import Customer
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
import datetime
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)

def index(request):
    # Lấy tham số sắp xếp và tìm kiếm từ URL
    search_query = request.GET.get('q', '').strip()
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

    # Thêm logic tìm kiếm theo tên khách sạn
    if search_query:
        rooms = rooms.filter(Q(hotel_name__icontains=search_query))
    
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
    
    rooms = rooms.order_by('price')

    context = {
        'rooms': rooms,
        'current_sort': sort_by,
        'current_order': order,
        'min_price': min_price or '',
        'max_price': max_price or '',
        'search_query': search_query,
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
        
        #Lấy tiêu chí sắp xếp từ request (nếu có), mặc định là theo tên
        sort_by = request.POST.get('sort_by', 'name')
        order_direction = request.POST.get('order', 'asc')
        
        #Them dieu kien sap xep
        order_field = sort_by if order_direction == 'asc' else f"-{sort_by}"
        
        # Thay đổi cách lấy dữ liệu, không dùng values()
        data = Rooms.objects.filter(
            is_available=True,
            no_of_days_advance__gte=no_of_days,
            start_date__lte=start_date
        ).select_related('manager').order_by('-price')
        
        request.session['no_of_days']=no_of_days
        return render(request,'booking/book.html',{
            'data': data,
            'start_date': start_date,
            'end_date': end_date,
            'no_of_days': no_of_days
        })
    else:
        return redirect('index')

def book_now(request, id):
    if not request.session.get("username"):
        next = "book-now/" + str(id)
        return redirect('user_login')
        
    if request.session.get("type") != 'customer':
        return redirect('index')

    try:
        data = Rooms.objects.get(id=id)
        
        # Lưu room_no vào session
        request.session['room_no'] = id
        
        # Lấy ngày từ session nếu có
        start_date = request.session.get('start_date')
        end_date = request.session.get('end_date')
        no_of_days = request.session.get('no_of_days', 0)
        
        # Tính giá ban đầu
        bill = data.price * int(no_of_days) if no_of_days else 0
        deposit = bill * 0.5 if bill else 0
        
        # Lưu bill vào session
        request.session['bill'] = bill
        request.session['deposit'] = deposit
        
        try:
            roomManager = data.manager.username
        except (Customer.DoesNotExist, AttributeError):
            roomManager = "Not assigned"
        
        context = {
            "no_of_days": no_of_days,
            "room_no": data.room_no,
            "data": data,
            "bill": bill,
            "deposit": deposit,
            "roomManager": roomManager,
            "start": start_date,
            "end": end_date,
            "has_dates": bool(start_date and end_date)
        }
        
        return render(request, "booking/book-now.html", context)
        
    except Rooms.DoesNotExist:
        messages.error(request, "Phòng không tồn tại")
        return redirect("index")

def book_confirm(request):
    if request.method == "POST":
        try:
            payment_method = request.POST.get('payment_method')
            
            # Lấy dữ liệu từ session
            room_no = request.session.get('room_no')
            start_date = request.session.get('start_date')
            end_date = request.session.get('end_date')
            amount = request.session.get('bill')
            
            if not all([room_no, start_date, end_date, amount]):
                messages.error(request, "Thiếu thông tin đặt phòng")
                return redirect('index')
            
            username = request.session['username']
            user_id = Customer.objects.get(username=username)
            room = Rooms.objects.get(id=room_no)
            
            if payment_method == 'online':
                payment_gateway = request.POST.get('payment_gateway')
                deposit = request.session.get('deposit')
                
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
            
        except Exception as e:
            messages.error(request, f"Có lỗi xảy ra: {str(e)}")
            return redirect('index')
    
    return redirect('index')

def cancel_room(request, id):
    try:
        logger.debug(f"Attempting to cancel booking {id}")
        data = Booking.objects.get(id=id)
        
        # Log thông tin booking
        logger.debug(f"Booking found: {data}")
        logger.debug(f"Current user: {request.session.get('username')}")
        logger.debug(f"Booking user: {data.user_id.username}")
        
        # Kiểm tra xem người dùng có quyền hủy booking này không
        if request.session.get('username') == data.user_id.username:
            room = data.room_no
            room.is_available = True
            room.save()
            data.delete()
            logger.debug("Booking cancelled successfully")
            return JsonResponse({'status': 'success', 'message': 'Đã hủy đặt phòng thành công'})
        else:
            logger.warning("Unauthorized cancellation attempt")
            return JsonResponse({'status': 'error', 'message': 'Bạn không có quyền hủy đặt phòng này'})
    except Booking.DoesNotExist:
        logger.error(f"Booking {id} not found")
        return JsonResponse({'status': 'error', 'message': 'Không tìm thấy booking'})
    except Exception as e:
        logger.error(f"Error cancelling booking: {str(e)}")
        return JsonResponse({'status': 'error', 'message': f'Lỗi: {str(e)}'})

def delete_room(request,id):
    data=Rooms.objects.get(id=id)
    manager=data.manager.username
    if manager==request.session['username']:
        data.delete()
        return HttpResponse("You have deleted the room successfully")
    else:
        return HttpResponse("Invalid Request")


            



    
