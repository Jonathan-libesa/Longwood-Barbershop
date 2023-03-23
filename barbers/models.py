from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


SERVICE_CHOICES = (
    ("Kadihm M", "Kadihm M"),
    ("Azad Z", "Azad Z"),
    ("George S", "George S"),
    )

TIME_CHOICES = (
    ("8 AM", "8 AM"),
    ("8:30AM", "8:30AM"),
    ("10AM", "10AM"),
    ("12:30PM", "12:30PM"),
    ("1:30PM", "1:30PM"),
    ("2:30PM", "2:30PM"),
    ("3 PM", "3 PM"),
    ("3:30 PM", "3:30 PM"),
    ("4 PM", "4 PM"),
    ("4:30 PM", "4:30 PM"),
    ("5 PM", "5 PM"),
    ("5:30 PM", "5:30 PM"),
    ("6 PM", "6 PM"),
    ("6:30 PM", "6:30 PM"),
    ("7 PM", "7 PM"),
    ("7:30 PM", "7:30 PM"),
)

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES, default="Kadihm M")
    day = models.DateField(default=datetime.now)
    time = models.CharField(max_length=10, choices=TIME_CHOICES, default="8 AM")
    time_ordered = models.DateTimeField(default=datetime.now, blank=True)
    #contact=models.CharField(max_length=10,blank=False)

    def __str__(self):
      return f"{self.user.username} | day: {self.day} | time: {self.time}"

