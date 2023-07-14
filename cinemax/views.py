from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import messages
from datetime import date
from django.shortcuts import get_object_or_404
from .models import Movie, Profile, Ticket, Transaction
from django.urls import reverse
from django.contrib.auth.decorators import login_required

import requests

# Create your views here.
def homepage(request):
    # get all movies
    all_movies = Movie.objects.all()
    # create a dictionary to track unique movie titles
    unique_titles = {}
    # iterate over movies to filter out duplicates
    for movie in all_movies:
        unique_titles[movie.title] = movie.id
    # retrieve unique movies based on filtered titles
    unique_movies = Movie.objects.filter(id__in=unique_titles.values())

    return render(request, 'homepage.html', {'movies': unique_movies})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() 
            # fetch the data from the form
            email = request.POST['email']
            age = request.POST['age']
            full_name = request.POST['fullname']

            user.first_name = full_name
            user.email = email
            user.save()

            # save the age in user profile
            profile, created = Profile.objects.get_or_create(user=user)
            profile.age = age
            profile.save()

            login(request, user)
            return redirect('homepage')
        else:
            errors = form.errors
            return render(request, 'register.html', {'errors': errors})

    return render(request, 'register.html')

def loginview(request):
    form = UserCreationForm(request.POST)
    if request.user.is_authenticated:
        return redirect('homepage') 

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.is_staff:  
                return redirect('admin_page')
            else:
                return redirect('homepage')

        else:
            # can u render error like in register
            messages.info(request, f'Username OR password is incorrect')
            return render(request, 'login.html')
    elif request.method == 'GET': 
        return render(request, 'login.html')

def logoutview(request):
    logout(request)
    return redirect('homepage')

def movie_list(request):
    url = 'https://seleksi-sea-2023.vercel.app/api/movies'
    response = requests.get(url)
    movies_data = response.json()

    for movie_data in movies_data:
        movie = Movie.objects.create(
            title=movie_data['title'],
            description=movie_data['description'],
            age_rating=movie_data['age_rating'],
            poster=movie_data['poster_url'],
            ticket_price=movie_data['ticket_price']
        )
        movie.save()

    return render(request, 'movie_list.html', {'movies': movies_data})

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    return render(request, 'movie_detail.html', {'movie': movie})

def withdraw(request):
    if request.method == 'POST':
        amount = int(request.POST['amount'])
        profile = Profile.objects.get(user=request.user)
        if profile.balance >= amount:
            profile.balance -= amount
            profile.save()
            # Add any additional logic or redirect as needed
        else:
            messages.info(request, f'Insufficient Balance')
    return redirect('homepage')

def top_up(request):
    if request.method == 'POST':
        amount = int(request.POST['amount'])
        profile = Profile.objects.get(user=request.user)
        profile.balance += amount
        profile.save()
        # Add any additional logic or redirect as needed
    return redirect('homepage')

def book_ticket(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    profile = Profile.objects.get(user=request.user)
    booked_seats = Ticket.objects.filter(movie=movie, date=date.today()).values_list('seats', flat=True)

    # Parsing seat_number dari database
    booked_seat_numbers = set()
    for booked_seat in booked_seats:
        seat_numbers = booked_seat.split(',')
        booked_seat_numbers.update(seat_numbers)

    # Check avaible seats
    seats = []
    for seat in range(1, 65):
        if str(seat) in booked_seat_numbers:
            seats.append({'number': seat, 'available': False})
        else:
            seats.append({'number': seat, 'available': True})

    if request.method == 'POST':
        age = request.user.profile.age
        name = request.user.first_name

        selected_seats = []
        for seat in request.POST.getlist('seats'):
            try:
                seat_number = int(seat.split('_')[1])
                selected_seats.append(seat_number)
            except (IndexError, ValueError):
                messages.error(request, "Invalid seat selection. Please try again.")
                return redirect('book_ticket', movie_id=movie_id)

        if len(selected_seats) > 6:
            messages.error(request, "You can book a maximum of 6 tickets per transaction.")
            return redirect('book_ticket', movie_id=movie_id)

        # Check if user's age is below movie's age rating
        if  request.user.profile.age < int(movie.age_rating):
            messages.error(request, "You are not old enough to book tickets for this movie.")
            return redirect('book_ticket', movie_id=movie_id)

        # Calculate total cost based on ticket price and number of tickets
        total_cost = movie.ticket_price * len(selected_seats)

        # Create a new ticket
        ticket = Ticket.objects.create(user=request.user, movie=movie, seats=",".join(str(seat) for seat in selected_seats), total_cost=total_cost)
    
        if profile.balance >= total_cost:
            profile.balance -= total_cost
            profile.save()
            transaction = Transaction.objects.create(ticket=ticket, name=name, age=profile.age, payment_status=True)
            return redirect('history')
        else:
            messages.error(request, "Insufficient balance. Please top up your balance First.")
            return redirect('book_ticket', movie_id=movie_id)
    
    else:
        return render(request, 'booking.html', {'movie': movie, 'seats': seats, 'profile': profile, 'total_cost': 0, 'selected_seats': []})

def payment(request, ticket_id):
    ticket = Ticket.objects.get(pk=ticket_id)
    total_cost = ticket.total_cost
    profile = Profile.objects.get(user=request.user)
    transaction = Transaction.objects.create(ticket=ticket, name=request.user.username, age=profile.age)

    if request.method == 'POST':
        profile.balance -= total_cost
        profile.save()
        transaction.payment_status = True
        transaction.save()
        return redirect('homepage')

    return render(request, 'payment.html', {'ticket': ticket, 'total_cost': total_cost, 'profile': profile})

def cancel_booking(request, ticket_id):
    ticket = Ticket.objects.get(pk=ticket_id)
    ticket.delete()
    messages.success(request, "Booking canceled successfully.")
    return redirect('homepage')


@login_required
def history(request):
    transactions = Transaction.objects.filter(payment_status=True, ticket__user=request.user)
    return render(request, 'history.html', {'transactions': transactions})

def cancel_ticket(request, ticket_id):
    ticket = Ticket.objects.get(pk=ticket_id)
    profile = Profile.objects.get(user=request.user)

    profile.balance += ticket.total_cost
    profile.save()
    
    ticket.delete()
    
    messages.success(request, "Ticket canceled successfully. The refund has been added to your balance.")
    return redirect('history')

