from django.db import models
from django.contrib.auth.models import User


class UserDetails(models.Model):
    user_id = models.OneToOneField(User)
    deleted = models.BooleanField(default=False)
    birth_day = models.DateField('birth date')
    image = models.ImageField('photo')
    amount = models.IntegerField('money')


class Performance(models.Model):
    date = models.DateField('date of performance')
    time = models.TimeField('time of performance')
    description = models.TextField(max_length=1000)


class Ticket(models.Model):
    status = models.CharField(max_length=16)
    price = models.FloatField('price')
    performance_id = models.ForeignKey(
        Performance,
        related_name='performance',
        on_delete=models.CASCADE,
        null=False,
        blank=False
        )
    booked = models.DateTimeField(
        null=True,
        blank=True
    )
    bought = models.DateTimeField(
        null=True,
        blank=True
    )
    booked_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='booked_by'
        )
    bought_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='bought_by'
        )


class Feature(models.Model):
    feature = models.CharField(max_length=16)
    performance_id = models.ManyToManyField(Performance)


class Discount(models.Model):
    code = models.CharField(max_length=12)
    percent = models.IntegerField('discount percentage')
    ticket_id = models.OneToOneField(Ticket)


class TicketHistory(models.Model):
    datetime = models.DateTimeField()
    message = models.CharField(max_length=30)
    ticket_id = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        blank=False,
        null=False
        )
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True
        )


class UserFeature(models.Model):
    feature_name = models.CharField(max_length=16)


class FeatureIncompatibility(models.Model):
    feature_id = models.ForeignKey(
        Feature,
        blank=False,
        null=False)
    user_feature_id = models.ForeignKey(
        UserFeature,
        blank=False,
        null=False)


# class PerformanceFeature(models.Model):
#     performance_id = models.ForeignKey(
#         Performance,
#         on_delete=models.SET_NULL,
#         blank=True,
#         null=True)
#     feature_id = models.ForeignKey(
#         Feature,
#         on_delete=models.SET_NULL,
#         blank=True,
#         null=True)
