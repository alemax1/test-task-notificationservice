import pytz as pytz
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


class Mailing(models.Model):
    date_start = models.DateTimeField()
    date_finish = models.DateTimeField()
    time_start = models.TimeField()
    time_finish = models.TimeField()
    mailing_message = models.TextField(max_length=255)
    tag = models.CharField(max_length=100, blank=True)
    phone_number_code = models.CharField(max_length=3, blank=True)

    @property
    def sending(self):
        now = timezone.now()
        if self.date_start <= now <= self.date_finish:
            return True
        else:
            return False

    def __str__(self):
        return self.tag


class Client(models.Model):
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    phone_regex = RegexValidator(regex=r'^7\d{10}$', message="Phone number format is : 7XXXXXXXXXX")
    phone_number = models.CharField(validators=[phone_regex], unique=True, max_length=11)
    phone_number_code = models.CharField(max_length=3, editable=False)
    client_tag = models.CharField(max_length=100, blank=True)
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='UTC')

    def save(self, *args, **kwargs):
        self.phone_number_code = str(self.phone_number)[1:4]
        return super(Client, self).save(*args, **kwargs)

    def __str__(self):
        return self.phone_number


class Message(models.Model):
    SEND = "send"
    NOT_SEND = "not send"

    STATUS_CHOICES = [
        (SEND, "Send"),
        (NOT_SEND, "Not send"),
                    ]

    time_create = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, null=True)
    message_mailing = models.ForeignKey('Mailing', on_delete=models.CASCADE)
    client = models.ForeignKey('Client', on_delete=models.CASCADE)

    def __str__(self):
        return self.client
