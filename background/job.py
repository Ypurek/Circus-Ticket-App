import logging
from apscheduler.schedulers.background import BackgroundScheduler
from core.processing import release_bookings_by_timeout, delete_tickets_until



def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(release_bookings_by_timeout, 'interval', minutes=1)
    scheduler.add_job(delete_tickets_until, 'interval', minutes=1)
    scheduler.start()
