from django.contrib import admin
from .models import Profile,Ticket, Transaction

# Register your models here.
admin.site.register(Profile)
admin.site.register(Ticket)
admin.site.register(Transaction)
