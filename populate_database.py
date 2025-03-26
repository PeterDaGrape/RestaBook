import os
import django
import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RestaBook.settings')
django.setup()

from app.models import User, Cuisine, Restaurant, Booking, Review, StandardHours, CustomHours

def populate():
    # Create test users
    user1 = User.objects.create_user(username='john_doe', email='john@example.com', password='password', isManager=False)
    user2 = User.objects.create_user(username='jane_smith', email='jane@example.com', password='password', isManager=False)
    
    # Create managers
    manager1 = User.objects.create_user(username='alice_manager', email='alice@example.com', password='password', isManager=True)
    manager2 = User.objects.create_user(username='bob_manager', email='bob@example.com', password='password', isManager=True)
    
    # Create cuisines
    cuisine1 = Cuisine.objects.create(name='Italian')
    cuisine2 = Cuisine.objects.create(name='Chinese')
    
    # Create restaurants
    restaurant1 = Restaurant.objects.create(
        cuisine=cuisine1,
        manager=manager1,
        name='Italian Bistro',
        email='contact@italianbistro.com',
        address='123 Main St',
        phone='123-456-7890'
    )
    
    restaurant2 = Restaurant.objects.create(
        cuisine=cuisine2,
        manager=manager2,
        name='Chinese Delight',
        email='contact@chinesedelight.com',
        address='456 Elm St',
        phone='987-654-3210'
    )


    r1_st_hours = StandardHours.objects.create(
        restaurant = restaurant1,
        number_tables = 10,
        opening_time = datetime.time(hour=9,minute=30),
        closing_time = datetime.time(hour=22,minute=30),
        week_day = "Friday"
    )

    # Additional standard hours for restaurant2
    r2_st_hours = StandardHours.objects.create(
        restaurant=restaurant2,
        number_tables=15,
        opening_time=datetime.time(hour=10, minute=0),
        closing_time=datetime.time(hour=23, minute=0),
        week_day="Saturday"
    )

    # Standard hours for each day of the week for restaurant1
    StandardHours.objects.create(
        restaurant=restaurant1,
        number_tables=10,
        opening_time=datetime.time(hour=9, minute=30),
        closing_time=datetime.time(hour=22, minute=30),
        week_day="Monday"
    )
    StandardHours.objects.create(
        restaurant=restaurant1,
        number_tables=10,
        opening_time=datetime.time(hour=9, minute=30),
        closing_time=datetime.time(hour=22, minute=30),
        week_day="Tuesday"
    )
    StandardHours.objects.create(
        restaurant=restaurant1,
        number_tables=10,
        opening_time=datetime.time(hour=9, minute=30),
        closing_time=datetime.time(hour=22, minute=30),
        week_day="Wednesday"
    )
    StandardHours.objects.create(
        restaurant=restaurant1,
        number_tables=10,
        opening_time=datetime.time(hour=9, minute=30),
        closing_time=datetime.time(hour=22, minute=30),
        week_day="Thursday"
    )
    StandardHours.objects.create(
        restaurant=restaurant1,
        number_tables=10,
        opening_time=datetime.time(hour=9, minute=30),
        closing_time=datetime.time(hour=22, minute=30),
        week_day="Saturday"
    )
    StandardHours.objects.create(
        restaurant=restaurant1,
        number_tables=10,
        opening_time=datetime.time(hour=9, minute=30),
        closing_time=datetime.time(hour=22, minute=30),
        week_day="Sunday"
    )

    # Standard hours for each day of the week for restaurant2
    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Sunday"]:
        StandardHours.objects.create(
            restaurant=restaurant2,
            number_tables=15,
            opening_time=datetime.time(hour=10, minute=0),
            closing_time=datetime.time(hour=23, minute=0),
            week_day=day
        )
    StandardHours.objects.create(
        restaurant=restaurant2,
        number_tables=15,
        opening_time=datetime.time(hour=10, minute=0),
        closing_time=datetime.time(hour=23, minute=0),
        week_day="Saturday"
    )

    # Custom hours for restaurant1
    r1_custom_hours = CustomHours.objects.create(
        restaurant=restaurant1,
        date=datetime.date(2023, 12, 25),
        opening_time=datetime.time(hour=12, minute=0),
        closing_time=datetime.time(hour=20, minute=0),
        number_tables=8
    )

    # Additional custom hours for the coming weeks
    CustomHours.objects.create(
        restaurant=restaurant1,
        date=datetime.date(2023, 10, 20),
        opening_time=datetime.time(hour=11, minute=0),
        closing_time=datetime.time(hour=21, minute=0),
        number_tables=8
    )
    CustomHours.objects.create(
        restaurant=restaurant2,
        date=datetime.date(2023, 10, 21),
        opening_time=datetime.time(hour=12, minute=0),
        closing_time=datetime.time(hour=22, minute=0),
        number_tables=12
    )

    # Create reviews
    review1 = Review.objects.create(
        restaurant=restaurant1,
        user=user1,
        star_rating=5,
        text="Amazing food and great service!",
        review_date=datetime.date(2023, 10, 1)
    )
    review2 = Review.objects.create(
        restaurant=restaurant2,
        user=user2,
        star_rating=4,
        text="Delicious food but a bit crowded.",
        review_date=datetime.date(2023, 10, 2)
    )

    # Create bookings
    booking1 = Booking.objects.create(
        restaurant=restaurant1,
        user=user1,
        date=datetime.date(2023, 10, 15),
        time=datetime.time(hour=19, minute=0),
    )
    booking2 = Booking.objects.create(
        restaurant=restaurant2,
        user=user2,
        date=datetime.date(2023, 10, 16),
        time=datetime.time(hour=20, minute=0),
    )

    print("Database populated with test data.")

if __name__ == '__main__':
    populate()