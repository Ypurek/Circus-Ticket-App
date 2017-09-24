from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from core.models import Ticket, Performance, Feature, TicketHistory, AppSettings, UserFeature, UserDetails
from core.exceptions import AppPropertyNotSet
from core import processing
import datetime


class TestFeature(TestCase):
    def setUp(self):
        Feature.objects.create(feature='dog')

    def test_feature_can_be_added(self):
        result = processing.add_feature('cat')
        self.assertEqual(result[0].feature, 'cat')
        self.assertEqual(result[1], True)

    def test_feature_cannot_be_added_twice(self):
        result = processing.add_feature('dog')
        self.assertEqual(result[0].feature, 'dog')
        self.assertEqual(result[1], False)


class TestTicketFlow(TestCase):
    login = 'testUser'
    date = datetime.date(2020, 1, 1)
    time1 = datetime.time(12, 0)
    time2 = datetime.time(13, 0)
    time3 = datetime.time(14, 0)
    time4 = datetime.time(15, 0)

    def setUp(self):
        processing.set_app_property('booking_timeout', '15')
        user = User.objects.create_user(self.login, 'aaa@bbb.com', '123')
        p1 = processing.add_performance(self.date, self.time1, '', [])
        p2 = processing.add_performance(self.date, self.time2, '', [])
        p3 = processing.add_performance(self.date, self.time3, '', [])
        p4 = processing.add_performance(self.date, self.time4, '', [])
        processing.add_tickets(performance=p1, price=100)
        processing.add_tickets(performance=p2, price=100)
        processing.add_tickets(performance=p3, price=100)
        Ticket.objects.create(status='booked', price=1, booked=timezone.now() - datetime.timedelta(minutes=20), booked_by=user, performance_id=p4)

    def test_ticket_book(self):
        user = User.objects.get_by_natural_key(self.login)
        tickets = processing.get_tickets(date_from=self.date, time_from=self.time1, time_to=self.time1)
        ticket = processing.book_ticket(user, tickets[0])
        record = TicketHistory.objects.get(ticket_id=ticket)
        self.assertEqual(ticket.status, 'booked', 'ticket not booked')
        self.assertEqual(ticket.booked_by, user, 'booked by not saved correctly')
        self.assertEqual(record.user_id, user, 'info not saved in history')

    def test_ticket_buy(self):
        user = User.objects.get_by_natural_key(self.login)
        tickets = processing.get_tickets(date_from=self.date, time_from=self.time2, time_to=self.time2)
        ticket = processing.buy_ticket(user, tickets[0])
        record = TicketHistory.objects.get(ticket_id=ticket)
        self.assertEqual(ticket.status, 'bought', 'ticket not bought')
        self.assertEqual(ticket.bought_by, user, 'bought by not saved correctly')
        self.assertEqual(record.user_id, user, 'info not saved in history')

    def test_ticket_buyback(self):
        user = User.objects.get_by_natural_key(self.login)
        tickets = processing.get_tickets(date_from=self.date, time_from=self.time3, time_to=self.time3)
        ticket = processing.book_ticket(user, tickets[0])
        ticket = processing.buyback_ticket(user, ticket)
        records = TicketHistory.objects.filter(ticket_id=ticket).order_by('datetime')
        self.assertEqual(ticket.status, 'bought', 'ticket not bought back')
        self.assertEqual(ticket.bought_by, user, 'bought by not saved correctly')
        self.assertEqual(records[1].user_id, user, 'info not saved in history')

    def test_ticket_release(self):
        processing.release_bookings();
        tickets = processing.get_tickets(date_from=self.date, time_from=self.time4, time_to=self.time4)
        record = TicketHistory.objects.get(ticket_id=tickets[0])
        self.assertEqual(tickets[0].status, 'available', 'ticket not released')
        self.assertIsNone(tickets[0].booked_by, 'booked by not cleared')
        self.assertIsNone(tickets[0].booked, 'booked not cleared')
        self.assertTrue('released' in record.message, 'info not saved in history')


class TestProperties(TestCase):
    def setUp(self):
        processing.set_app_property('new_property', 'value')
        processing.set_app_property('new_property2', 'value')

    def test_get_property(self):
        value = processing.get_app_property('new_property')
        self.assertEqual(value, 'value')

    def test_set_property(self):
        processing.set_app_property('new_property2', 'modified value')
        value = processing.get_app_property('new_property2')
        prop = AppSettings.objects.filter(property='new_property2')
        self.assertEqual(value, 'modified value', 'property value not updated')
        self.assertEqual(len(prop), 1, 'property duplicated')

    def test_property_does_not_exist(self):
        marker = False
        try:
            processing.get_app_property('propert?')
        except AppPropertyNotSet:
            marker = True
        finally:
            self.assertTrue(marker, 'exception not raised')


class TestDiscount(TestCase):
    code = None
    # 1 - discount code, 2 - user logged in, 3 - 10th user, 4 - expected result
    expected = ((False, False, '1', 0),
                (False, False, '0', 1),
                (False, True, '1', 3),
                (False, True, '0', 4),
                (True, False, '1', 5),
                (True, False, '0', 6),
                (True, True, '1', 5),
                (True, True, '0', 6))

    def setUp(self):
        self.code = processing.add_discount_code(5)
        processing.set_app_property('user_buy_counter', '1')
        processing.set_app_property('user_buy_counter_limit', '10')
        processing.set_app_property('user_buy_counter_discount', '1')
        processing.set_app_property('user_logged_in_discount', '3')

    def test_check_all_discount_combo(self):
        for case in self.expected:
            processing.set_app_property('user_buy_counter', case[2])
            result = processing.calculate_final_discount(discount_code=self.code if case[0] else None,
                                                is_user=case[1])
            self.assertEqual(result, case[3])

    def test_increment_counter_limited(self):
        processing.set_app_property('user_buy_counter', '9')
        processing.increment_user_counter_discount()
        actual = processing.get_app_property('user_buy_counter')
        self.assertEqual(actual, '0')

    def test_increment_counter_updated(self):
        processing.set_app_property('user_buy_counter', '5')
        processing.increment_user_counter_discount()
        actual = processing.get_app_property('user_buy_counter')
        self.assertEqual(actual, '6')


class TestPricing(TestCase):
    disc_code = None
    ticket = None
    feature = None
    user = None
    # 0 - is user logged in, 1 - discount code, 2 - user feature, 3 - snack, 4 - expected result
    expected = ((False, False, False, False, 100),
                (False, False, False, True, 150),
                (False, False, True, False, 130),
                (False, False, True, True, 180),
                (False, True, False, False, 95),
                (False, True, False, True, 142.5),
                (False, True, True, False, 123.5),
                (False, True, True, True, 171),
                (True, False, False, False, 97),
                (True, False, False, True, 145.5),
                (True, False, True, False, 126.1),
                (True, False, True, True, 174.6),
                (True, True, False, False, 95),
                (True, True, False, True, 142.5),
                (True, True, True, False, 123.5),
                (True, True, True, True, 171))

    def setUp(self):
        processing.set_app_property('user_buy_counter', '1')
        processing.set_app_property('user_buy_counter_limit', '10')
        processing.set_app_property('user_buy_counter_discount', '1')
        processing.set_app_property('user_logged_in_discount', '3')
        processing.set_app_property('snack_price', '50')
        self.disc_code = processing.add_discount_code(5)
        self.ticket = Ticket(status='available', price=100)
        self.feature = UserFeature(feature_name='dog', price=30)
        self.user = User.objects.create_user('buyer')
        details = UserDetails(user_id=self.user, amount=200)
        details.save()

    def test_price_calculation(self):
        for case in self.expected:
            price = processing.get_total_price(self.ticket, case[0],
                                               self.disc_code if case[1] else None,
                                               self.feature if case[2] else None,
                                               case[3])
            self.assertEqual(price, case[4], 'price calculated wrong')

    def test_debit_ok(self):
        result = processing.debit(self.user, self.ticket, 100)
        self.assertTrue(result, 'purchase failed')

    def test_debit_nok(self):
        result = processing.debit(self.user, self.ticket, 300)
        self.assertFalse(result, 'purchase done')