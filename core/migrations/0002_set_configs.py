# Manually created to set init data
from django.db import migrations
from core import processing


def set_settings(apps, schema_editor):
    processing.set_app_property('max_book_ticket', '10')
    processing.set_app_property('user_buy_counter', '1')
    processing.set_app_property('user_buy_counter_limit', '10')
    processing.set_app_property('user_buy_counter_discount', '1')
    processing.set_app_property('user_logged_in_discount', '3')
    processing.set_app_property('snack_price', '50')
    processing.set_app_property('booking_timeout', '5')


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(set_settings)
    ]
