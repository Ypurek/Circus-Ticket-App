# Manually created to set init data
from django.db import migrations
from core import processing
from core.models import Feature, UserFeature
import datetime as dt


def add_restrictions(apps, schema_editor):
    UserFeature.objects.create(name='cat', price=50, incompatible_with=Feature.objects.get(feature='dogs'))
    UserFeature.objects.create(name='mouse', price=50, incompatible_with=Feature.objects.get(feature='elephants'))
    UserFeature.objects.create(name='parrot', price=50, incompatible_with=None)


def create_performances(apps, schema_editor):
    dogs_show = {'name': 'Шоу Собак',
                 'description': 'Найвідоміше у світі шоу собак. Вони танцюють, стрибають і граються з клоунами. Не пропустіть!',
                 'features': ['dogs', 'clowns']}
    performance = processing.add_performance(date=dt.date(2035, 5, 5),
                                             time=dt.time(11, 0),
                                             price=100,
                                             **dogs_show)
    processing.add_tickets(performance, 30)
    performance = processing.add_performance(date=dt.date(2035, 5, 6),
                                             time=dt.time(12, 0),
                                             price=100,
                                             **dogs_show)
    processing.add_tickets(performance, 40)
    performance = processing.add_performance(date=dt.date(2035, 5, 6),
                                             time=dt.time(13, 0),
                                             price=200,
                                             **dogs_show)
    processing.add_tickets(performance, 20)

    africa = {'name': 'Казки Африки',
              'description': 'Відправляйтесь з нами в пригоду на спекотний континент! В програмі леви, крокодили та слони!',
              'features': ['lions', 'crocs', 'elephants']}
    performance = processing.add_performance(date=dt.date(2035, 6, 10),
                                             time=dt.time(15, 0),
                                             price=400,
                                             **africa)
    processing.add_tickets(performance, 20)
    africa = {'name': 'Казки Африки',
              'description': 'Відправляйтесь з нами в пригоду на спекотний континент! В програмі леви, крокодили та слони!',
              'features': ['lions', 'crocs', 'elephants']}
    performance = processing.add_performance(date=dt.date(2035, 6, 15),
                                             time=dt.time(18, 0),
                                             price=300,
                                             **africa)
    processing.add_tickets(performance, 30)
    alice = {'name': 'Аліса в країні казок',
             'description': 'Щоу для дітей! Відправляйтесь у подорож з Алісою та насолоджуйтесь виставою повітряних гімнастів та акробатів',
             'features': ['acrobats']}
    performance = processing.add_performance(date=dt.date(2035, 9, 25),
                                             time=dt.time(12, 0),
                                             price=300,
                                             **alice)
    processing.add_tickets(performance, 30)
    alice = {'name': 'Аліса в країні казок',
             'description': 'Щоу для дітей! Відправляйтесь у подорож з Алісою та насолоджуйтесь виставою повітряних гімнастів та акробатів',
             'features': ['acrobats']}
    performance = processing.add_performance(date=dt.date(2035, 10, 26),
                                             time=dt.time(16, 0),
                                             price=400,
                                             **alice)
    processing.add_tickets(performance, 20)


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('core', '0002_set_data')
    ]

    operations = [
        migrations.RunPython(create_performances),
        migrations.RunPython(add_restrictions)
    ]
