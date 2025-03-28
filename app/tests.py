from django.test import TestCase, Client
from django.urls import reverse
from app.models import User, Restaurant, StandardHours, CustomHours, Booking, Cuisine

class ManageRestaurantViewTests(TestCase):
    def setUp(self):
        # Create manager 
        self.manager = User.objects.create_user(username='manager', password='password', isManager=True)
        
        # Create cuisine
        self.cuisine = Cuisine.objects.create(name='Italian')
        
        # Create restaurant
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            email='test@example.com',
            address='123 Test St',
            phone='1234567890',
            cuisine=self.cuisine,
            manager=self.manager
        )
        
        self.client = Client()

    def test_manage_restaurant_access_by_manager(self):
        # Log in as the manager
        self.client.login(username='manager', password='password')
        
        # Access the manage restaurant page
        response = self.client.get(reverse('app:manage_restaurant', args=[self.restaurant.slug]))
        
        # Check if the page loads successfully
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Manager Admin Page for Test Restaurant')

    def test_manage_restaurant_access_by_non_manager(self):
        # Create a non-manager user
        user = User.objects.create_user(username='user', password='password', isManager=False)
        self.client.login(username='user', password='password')
        
        # Try to access the manage restaurant page
        response = self.client.get(reverse('app:manage_restaurant', args=[self.restaurant.slug]))
        
        # Check if access is forbidden
        self.assertEqual(response.status_code, 403)

    def test_edit_restaurant_details(self):
        # Log in as the manager
        self.client.login(username='manager', password='password')
        
        # Submit a POST request to edit restaurant details
        response = self.client.post(reverse('app:manage_restaurant', args=[self.restaurant.slug]), {
            'name': 'Updated Restaurant',
            'email': 'updated@example.com',
            'address': '456 Updated St',
            'phone': '9876543210',
            'cuisine': self.cuisine.id,
            'bookings_allowed': True
        })
        
        # Check if the restaurant details were updated
        self.restaurant.refresh_from_db()
        self.assertEqual(self.restaurant.name, 'Updated Restaurant')
        self.assertEqual(self.restaurant.email, 'updated@example.com')
        self.assertEqual(self.restaurant.address, '456 Updated St')
        self.assertEqual(self.restaurant.phone, '9876543210')

    def test_add_standard_hours(self):
        # Log in as the manager
        self.client.login(username='manager', password='password')
        
        # Submit a POST request to add standard hours
        response = self.client.post(reverse('app:add_standard_hours', args=[self.restaurant.slug]), {
            'number_tables': 10,
            'opening_time': '09:00',
            'closing_time': '17:00',
            'week_day': 'Monday',
            'bookings_allowed': True
        })
        
        # Check if the standard hours were added
        self.assertEqual(StandardHours.objects.count(), 1)
        standard_hour = StandardHours.objects.first()
        self.assertEqual(standard_hour.restaurant, self.restaurant)
        self.assertEqual(standard_hour.week_day, 'Monday')

    def test_add_custom_hours(self):
        # Log in as the manager
        self.client.login(username='manager', password='password')
        
        # Submit a POST request to add custom hours
        response = self.client.post(reverse('app:add_custom_hours', args=[self.restaurant.slug]), {
            'number_tables': 5,
            'opening_time': '10:00',
            'closing_time': '15:00',
            'date': '2025-03-28',
            'bookings_allowed': True
        })
        
        # Check if the custom hours were added
        self.assertEqual(CustomHours.objects.count(), 1)
        custom_hour = CustomHours.objects.first()
        self.assertEqual(custom_hour.restaurant, self.restaurant)
        self.assertEqual(custom_hour.date.strftime('%Y-%m-%d'), '2025-03-28')

class AddCustomHoursViewTests(TestCase):
    def setUp(self):
        self.manager = User.objects.create_user(username='manager', password='password', isManager=True)
        self.cuisine = Cuisine.objects.create(name='Italian')
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            email='test@example.com',
            address='123 Test St',
            phone='1234567890',
            cuisine=self.cuisine,
            manager=self.manager
        )
        self.client = Client()
 
    def test_add_custom_hours_success(self):
        self.client.login(username='manager', password='password')
        response = self.client.post(reverse('app:add_custom_hours', args=[self.restaurant.slug]), {
            'number_tables': 5,
            'opening_time': '10:00',
            'closing_time': '15:00',
            'date': '2025-03-28',
            'bookings_allowed': True
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertEqual(CustomHours.objects.count(), 1)