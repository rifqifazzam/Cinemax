## Features

- User Registration and Authentication: Users can register an account and log in to the application using their credentials. The authentication system is provided by Django's built-in authentication framework.

- Movie Listing: The application displays a list of available movies retrieved from an external API. The movies are stored in the database and include details such as title, description, age rating, poster image, and ticket price.

- Movie Details: Users can view detailed information about a specific movie, including its title, description, age rating, and ticket price.

- Ticket Booking: Authenticated users can select available seats for a specific movie and book them. The application validates the user's age against the movie's age rating to ensure eligibility. The total cost of the tickets is calculated based on the selected seats and ticket price. If the user has sufficient balance in their wallet, the booking is confirmed, and the total cost is deducted from the wallet balance.

- Wallet Management: Each user has a wallet balance associated with their account. Users can view their current balance and perform two actions: withdraw and top-up. The withdrawal functionality deducts a specified amount from the wallet balance if the balance is sufficient. The top-up functionality adds a specified amount to the wallet balance.

- Transaction History: Users can view their transaction history, which includes details of their ticket bookings. The history displays the  customer name, movie title, seat numbers, date, total cost, and an option to cancel the booking.

## Technologies Used

- Python
- Django
- HTML
- CSS
- JavaScript

## Installation

1. Clone the repository to your local machine. 
2. Install the project dependencies using `pip install -r requirements.txt`.
3. Run the database migrations using `python manage.py migrate`.
4. Start the development server using `python manage.py runserver`.

