from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    age = models.IntegerField(default=0)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class Ticket(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    movie = models.CharField(max_length=100)
    total_cost = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    

class Transaction(models.Model):
    ticket = models.ForeignKey(Ticket,on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.ticket.user.username
    

class User_seat(models.Model):
    ticket = models.ForeignKey(Ticket,on_delete=models.CASCADE)
    seat_number = models.IntegerField(default=0)
    movie_id = models.IntegerField(default=0)

    def __str__(self):
        return self.ticket.user.username

