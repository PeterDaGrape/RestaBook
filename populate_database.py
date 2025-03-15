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
        is_open = True,
        week_day = 3
    )
    
    print("Database populated with test data.")

if __name__ == '__main__':
    populate()