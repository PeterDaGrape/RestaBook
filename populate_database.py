import os
import django
import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RestaBook.settings')
django.setup()

from app.models import User, Cuisine, Restaurant, Booking, Review, StandardHours, CustomHours

def populate():
    User.objects.all().delete()

    # Create test users
    user1 = User.objects.create_user(username='john_doe', email='john@example.com', password='password', isManager=False)
    user2 = User.objects.create_user(username='jane_smith', email='jane@example.com', password='password', isManager=False)
    
    # Create managers
    manager1 = User.objects.create_user(username='alice_manager', email='alice@example.com', password='password', isManager=True)
    manager2 = User.objects.create_user(username='bob_manager', email='bob@example.com', password='password', isManager=True)
    manager3 = User.objects.create_user(username='charlie_manager', email='charlie@example.com', password='password', isManager=True)
    manager4 = User.objects.create_user(username='dave_manager', email='dave@example.com', password='password', isManager=True)
    manager5 = User.objects.create_user(username='eve_manager', email='eve@example.com', password='password', isManager=True)
    
    # Create cuisines
    cuisine1 = Cuisine.objects.create(name='Italian')
    cuisine2 = Cuisine.objects.create(name='Chinese')
    cuisine3 = Cuisine.objects.create(name='Mexican')
    
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
    
    restaurant3 = Restaurant.objects.create(
        cuisine=cuisine1,
        manager=manager3,
        name='Italian Cuisine',
        email='contact@italiancuisine.com',
        address='789 Oak St',
        phone='789-654-3210'
    )
    
    restaurant4 = Restaurant.objects.create(
        cuisine=cuisine2,
        manager=manager4,
        name='Chinese Feast',
        email='contact@chinesefeast.com',
        address='101 Pine St',
        phone='101-987-6543'
    )
    
    restaurant5 = Restaurant.objects.create(
        cuisine=cuisine3,
        manager=manager5,
        name='Mexican Grill',
        email='contact@mexicangrill.com',
        address='202 Maple St',
        phone='202-876-5432'
    )

    # Standard hours for each day of the week for restaurant1
    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
        StandardHours.objects.create(
            restaurant=restaurant1,
            number_tables=10,
            opening_time=datetime.time(hour=9, minute=30),
            closing_time=datetime.time(hour=22, minute=30),
            week_day=day
        )

    # Standard hours for each day of the week for restaurant2
    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
        StandardHours.objects.create(
            restaurant=restaurant2,
            number_tables=15,
            opening_time=datetime.time(hour=10, minute=0),
            closing_time=datetime.time(hour=23, minute=0),
            week_day=day
        )

    # Standard hours for each day of the week for restaurant3
    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
        StandardHours.objects.create(
            restaurant=restaurant3,
            number_tables=10,
            opening_time=datetime.time(hour=9, minute=30),
            closing_time=datetime.time(hour=22, minute=30),
            week_day=day
        )

    # Standard hours for each day of the week for restaurant4
    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
        StandardHours.objects.create(
            restaurant=restaurant4,
            number_tables=15,
            opening_time=datetime.time(hour=10, minute=0),
            closing_time=datetime.time(hour=23, minute=0),
            week_day=day
        )

    # Standard hours for each day of the week for restaurant5
    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
        StandardHours.objects.create(
            restaurant=restaurant5,
            number_tables=12,
            opening_time=datetime.time(hour=11, minute=0),
            closing_time=datetime.time(hour=23, minute=0),
            week_day=day
        )

    # Create reviews for each restaurant
    Review.objects.create(
        restaurant=restaurant1,
        user=user1,
        star_rating=5,
        text="Amazing food and great service!",
        review_date=datetime.date(2023, 10, 1)
    )
    Review.objects.create(
        restaurant=restaurant2,
        user=user2,
        star_rating=4,
        text="Delicious food but a bit crowded.",
        review_date=datetime.date(2023, 10, 2)
    )

    Review.objects.create(
        restaurant=restaurant3,
        user=user1,
        star_rating=4,
        text="Great Italian cuisine, friendly staff!",
        review_date=datetime.date(2023, 10, 3)
    )
    Review.objects.create(
        restaurant=restaurant4,
        user=user2,
        star_rating=5,
        text="Impressive Chinese food and ambiance.",
        review_date=datetime.date(2023, 10, 4)
    )

    Review.objects.create(
        restaurant=restaurant5,
        user=user1,
        star_rating=5,
        text="Authentic Mexican dishes and lively atmosphere!",
        review_date=datetime.date(2023, 10, 5)
    )
    Review.objects.create(
        restaurant=restaurant5,
        user=user2,
        star_rating=4,
        text="Good food but the prices are a bit high.",
        review_date=datetime.date(2023, 10, 6)
    )

    print("Database populated with test data.")

if __name__ == '__main__':
    populate()
