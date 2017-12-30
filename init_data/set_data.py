from core import processing


def set_settings():
    processing.set_app_property('max_book_ticket', '10')
    processing.set_app_property('user_buy_counter', '1')
    processing.set_app_property('user_buy_counter_limit', '10')
    processing.set_app_property('user_buy_counter_discount', '1')
    processing.set_app_property('user_logged_in_discount', '3')
    processing.set_app_property('snack_price', '50')
    processing.set_app_property('booking_timeout', '15')
