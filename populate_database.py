import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RestaBook.settings')
django.setup()

from app.models import User, Cuisine, Restaurant, Booking, Review, StandardHours, CustomHours

def populate():
    # Create test users
    user1 = User.objects.create(name='John Doe', email='john@example.com', isManager=False)
    user2 = User.objects.create(name='Jane Smith', email='jane@example.com', isManager=False)
    
    # Create managers
    manager1 = User.objects.create(name='Alice Manager', email='alice@example.com', isManager=True)
    manager2 = User.objects.create(name='Bob Manager', email='bob@example.com', isManager=True)
    
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
    
    print("Database populated with test data.")

if __name__ == '__main__':
    populate()