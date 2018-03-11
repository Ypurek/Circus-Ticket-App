from django.urls import path
from . import views, testing_views, settings, error_views

urlpatterns = [
    path('', views.index, name='test'),
    path(settings.LOGIN_URL, views.auth_view, name='login'),
    path(settings.LOGOUT_URL, views.logout_view, name='logout'),
    path(settings.BOOKING_URL, views.booking, name='main'),
    path(settings.BOOK_URL, views.book, name='book'),
    path(settings.CLEAR_URL, views.clear_bookings, name='clear'),
    path(settings.BUY_INFO_URL, views.buy_info, name='buy_info'),
    path(settings.BUY_UPDATE_URL, views.update_price, name='update_price'),
    path(settings.BUY_FINAL_URL, views.process_payment, name='final_buy'),
    path('receipt/<int:id>/', views.get_receipt, name='receipt'),
    path('user/', views.user_info),
    path('user/update', views.user_update),
    path('payment/release/<int:id>', views.release_ticket),

    path('testing/', testing_views.service_view),
    path('testing/cards/', testing_views.credit_card_view),
    path('testing/discounts/', testing_views.discount_view),
    path('testing/history/', testing_views.ticket_history_view),
    path('testing/history/<int:number>', testing_views.ticket_history_view),

    path('400/', error_views.error400_view),
    path('403/', error_views.error403_view),
    path('404/', error_views.error404_view),
    path('500/', error_views.error500_view),
]
