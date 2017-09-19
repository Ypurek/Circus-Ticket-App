from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Ticket, Performance, Feature, TicketHistory
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
        p1 = processing.add_performance(self.date, self.time1, 'description', ['cat', 'dog'])
        p2 = processing.add_performance(self.date, self.time2, 'description', ['cat', 'dog'])
        p3 = processing.add_performance(self.date, self.time3, 'description', ['cat', 'dog'])
        p4 = processing.add_performance(self.date, self.time4, 'description', [])
        processing.add_tickets(p1, 100)
        processing.add_tickets(p2, 100)
        processing.add_tickets(p3, 100)
        user = User.objects.create_user(self.login, 'aaa@bbb.com', '123')
        Ticket.objects.create(status='available', price=1, booked=datetime.datetime.now() - datetime.timedelta(minutes=15), booked_by=user, performance_id=p4)

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
        self.assertEqual(len(tickets), 0)
        # record = TicketHistory.objects.get(ticket_id=tickets[0])
        # self.assertEqual(tickets[0].status, 'available', 'ticket not released')
        # self.assertEqual(tickets[0].booked_by, None, 'booked by not cleared')
        # self.assertEqual(tickets[0].booked, None, 'booked not cleared')
        # self.assertContains(record.message, 'released', 'info not saved in history')
