from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact-us', views.contact, name='contact'),
    path('book', views.book, name='book'),
    path('book-now/<int:id>', views.book_now, name='book_now'),
    path('book_confirm', views.book_confirm, name='book_confirm'),
    path('cancel-room/<int:id>', views.cancel_room, name='cancel_room'),
    path('delete_room/<int:id>', views.delete_room, name='delete_room'),
]