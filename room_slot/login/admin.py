from django.contrib import admin
from django.db.models import Sum
from django.utils.html import format_html
from login.models import Customer, RoomManager, Revenue
from booking.models import Contact, Rooms, Booking
from django.template.response import TemplateResponse

# Register your models here.
admin.site.register(Customer)
admin.site.register(RoomManager)
admin.site.register(Contact)
admin.site.register(Rooms)
admin.site.register(Booking)

@admin.register(Revenue)
class RevenueAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_bookings', 'display_revenue', 'display_profit', 'profit_percentage')
    list_filter = ('date',)
    change_list_template = 'admin/revenue_change_list.html'
    
    def display_revenue(self, obj):
        formatted_revenue = "{:,.2f}".format(float(obj.total_revenue))
        return format_html('<span style="color: #28a745;">₫{}</span>', formatted_revenue)
    display_revenue.short_description = 'Total Revenue'

    def display_profit(self, obj):
        formatted_profit = "{:,.2f}".format(float(obj.profit))
        return format_html('<span style="color: #17a2b8;">₫{}</span>', formatted_profit)
    display_profit.short_description = 'Profit'

    def profit_percentage(self, obj):
        if obj.total_revenue:
            percentage = (float(obj.profit) / float(obj.total_revenue)) * 100
            formatted_percentage = "{:.1f}".format(percentage)
            return format_html('<span style="color: #dc3545;">{}%</span>', formatted_percentage)
        return '0%'
    profit_percentage.short_description = 'Profit Margin'

    def changelist_view(self, request, extra_context=None):
        # Lấy dữ liệu cho biểu đồ
        chart_data = Revenue.objects.values('date', 'total_revenue', 'profit').order_by('date')
        revenue_data = [
            {
                'date': item['date'].strftime('%Y-%m-%d'), 
                'revenue': float(item['total_revenue']),
                'profit': float(item['profit'])
            } 
            for item in chart_data
        ]

        print("Revenue Data:", revenue_data)

        # Tính toán tổng số liệu
        total_stats = Revenue.objects.aggregate(
            total_revenue=Sum('total_revenue'),
            total_profit=Sum('profit'),
            total_bookings=Sum('total_bookings')
        )
        
        extra_context = extra_context or {}
        extra_context.update({
            'total_revenue': total_stats['total_revenue'],
            'total_profit': total_stats['total_profit'],
            'total_bookings': total_stats['total_bookings'],
            'chart_data': revenue_data
        })
        
        return super().changelist_view(request, extra_context=extra_context)

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
        js = ('https://cdn.jsdelivr.net/npm/chart.js',)