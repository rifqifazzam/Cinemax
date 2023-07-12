from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    age_rating = models.IntegerField()
    poster = models.URLField()
    ticket_price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    age = models.IntegerField(default=0)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class Ticket(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    movie = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    seats = models.CharField(max_length=100, default="")
    total_cost = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
    
class Transaction(models.Model):
    ticket = models.ForeignKey(Ticket,on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="")
    age = models.IntegerField(default=0)   
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        return self.name


