import logging
from apscheduler.schedulers.background import BackgroundScheduler
from core.processing import release_bookings_by_timeout, delete_tickets_until, \
    clear_discount_codes, clear_credit_cards, clear_ticket_history


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(release_bookings_by_timeout, 'interval', minutes=1)
    scheduler.add_job(delete_tickets_until, 'interval', minutes=1)
    scheduler.add_job(clear_discount_codes, 'cron', month='*', day='1st fri', hour=1)
    scheduler.add_job(clear_credit_cards, 'cron', month='*', day='1st fri', hour=1)
    scheduler.add_job(clear_ticket_history, 'cron', month='*', day='1st fri', hour=1)
    scheduler.start()
