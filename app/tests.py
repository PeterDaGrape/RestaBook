from django.test import TestCase, Client
from django.urls import reverse
from app.models import User, Restaurant, StandardHours, CustomHours, Booking, Cuisine, Review
from app.forms import UserForm
from datetime import date



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

    def test_add_custom_hours_invalid(self):
        self.client.login(username= 'manager', password='password')
        response = self.client.post(reverse('app:add_custom_hours', args=[self.restaurant.slug]),
        {'number_tables': '', #no # of tables added
        'opening_time': '10:00',
        'closing_time': '15:00',
        'date': '2025-03-28',
        'bookings_allowed': True
        })
        self.assertEqual(response.status_code, 200)  # Form re-rendered
        self.assertContains(response, 'This field is required.')
        self.assertEqual(CustomHours.objects.count(), 0)
 
class BookingsViewTests(TestCase):
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
 
        booking_user = User.objects.create_user(username='John Doe', email='john@example.com')
 
        self.booking = Booking.objects.create(
            restaurant=self.restaurant,
            user=booking_user,
            date='2025-03-28',
            time='12:00',
        )
 
        self.client = Client()
 
    def test_view_bookings(self):
        self.client.login(username='manager', password='password')
        response = self.client.get(reverse('app:manage_restaurant', args=[self.restaurant.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')
        self.assertContains(response, '12:00')
 
class UserFormsTests(TestCase):
    def test_user_form_valid(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword123'
        }
        form = UserForm(data=data)
        self.assertTrue(form.is_valid())
 
    def test_user_form_invalid(self):
        data = {
            'username': '',  # missing username
            'email': 'invalid-email',  # Invalid email format
            'password': 'short'  # Password short
        }
        form = UserForm(data=data)
        self.assertFalse(form.is_valid())
 
class ViewUserBookingsTests(TestCase):
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
        self.user = User.objects.create_user(username='john', email='john@example.com', password='password')
        self.booking = Booking.objects.create(
            restaurant=self.restaurant,
            user=self.user,
            date='2025-04-01',
            time='18:00'
        )
        self.client = Client()

class RestaurantModelTest(TestCase):

    def setUp(self):
        #Set up test data for the restaurant and reviews.#
        self.user = User.objects.create(username="testuser")
        self.cuisine = Cuisine.objects.create(name="Italian")
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            cuisine=self.cuisine,
            manager=self.user,
            email="test@example.com",
            address="123 Street",
            phone="1234567890",
        )

    def test_calculate_average_stars_no_reviews(self):
        #Test average when no reviews exist
        self.assertIsNone(self.restaurant.calculate_average_stars())

    def test_calculate_average_stars_single_review(self):
        #Test average when there is one review.#
        Review.objects.create(
            user=self.user, restaurant=self.restaurant, star_rating=4, text="Good", review_date=date.today()
        )
        self.assertEqual(self.restaurant.calculate_average_stars(), 4.0)

    def test_calculate_average_stars_multiple_reviews(self):
        #Test average with multiple reviews.#
        Review.objects.create(user=self.user, restaurant=self.restaurant, star_rating=5, text="Excellent", review_date=date.today())
        Review.objects.create(user=self.user, restaurant=self.restaurant, star_rating=3, text="Average", review_date=date.today())
        Review.objects.create(user=self.user, restaurant=self.restaurant, star_rating=4, text="Good", review_date=date.today())

        self.assertEqual(self.restaurant.calculate_average_stars(), 4.0)  # (5+3+4)/3 = 4.0

    def test_calculate_average_stars_with_invalid_ratings(self):
        #Ensure only valid ratings (0-5) are considered.#
        Review.objects.create(user=self.user, restaurant=self.restaurant, star_rating=5, text="Perfect", review_date=date.today())
        Review.objects.create(user=self.user, restaurant=self.restaurant, star_rating=3, text="Okay", review_date=date.today())
        Review.objects.create(user=self.user, restaurant=self.restaurant, star_rating=-1, text="Invalid", review_date=date.today())  # Should be ignored
        Review.objects.create(user=self.user, restaurant=self.restaurant, star_rating=6, text="Too high", review_date=date.today())  # Should be ignored

        self.assertEqual(self.restaurant.calculate_average_stars(), 4.0)  # (5+3)/2 = 4.0