from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', views.register, name='register'),
    path('login/', views.loginview, name='login'),
    path('logout/', views.logoutview, name='logout'),
    path('movies/', views.movie_list, name='movie_list'),  
    path('movies/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('top-up/', views.top_up, name='top_up'),
    path('book_ticket/<int:movie_id>/', views.book_ticket, name='book_ticket'),
    path('payment/<int:ticket_id>/', views.payment, name='payment'),
    path('cancel_booking/<int:ticket_id>/', views.cancel_booking, name='cancel_booking'),
    path('cancel-ticket/<int:ticket_id>/', views.cancel_ticket, name='cancel_ticket'),
    path('history/', views.history, name='history'),
]
