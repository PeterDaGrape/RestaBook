from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from app.forms import UserProfileForm, UserForm, RestaurantForm, StandardHoursForm, CustomHoursForm, BookingForm, ReviewForm
from app.models import Restaurant, Booking, CustomHours, Restaurant, StandardHours, Review, Cuisine
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from .forms import AvatarUploadForm
from django.contrib.auth import get_user_model

def register(request):
    registered = False
    User = get_user_model()  # Use the custom User model

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        username = request.POST.get('username')

        # Check if the username already exists

        # Validate both forms only if no username conflict exists
        if user_form.is_valid() and profile_form.is_valid():
            print('user valid')
            # Save the User object
            user = user_form.save(commit=False)
            user.set_password(user.password)  # Hash the password
            user.save()



            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'app/register.html', context={
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered,
    })

def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed
        # to request.POST['<variable>'], because the
        # request.POST.get('<variable>') returns None if the
        # value does not exist, while request.POST['<variable>']
        # will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)
        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # is the account active? it could have been disabled.
            if user.is_active:
                # if the account is valid and active, we can log the user in.
                # we'll send the user back to the homepage.
                login(request, user)
                return redirect(reverse('app:index'))
            else:
                # an inactive account was used - no logging in!
                return HttpResponse("Your RestaBook account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
            # The request is not a HTTP POST, so display the login form.
            # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'app/login.html')
    

def index(request):
    restaurant_list = Restaurant.objects.all()[:5]

    sorted_restaurants = sorted(restaurant_list, key=lambda restaurant: restaurant.calculate_average_stars(), reverse=True)
    context_dict = {}
    context_dict['restaurants'] = sorted_restaurants

    if request.user.is_authenticated:
        booking_count = Booking.objects.filter(user=request.user).count()
        context_dict['booking_count'] = booking_count
    response = render(request, 'app/index.html', context=context_dict)
    return response


# Use the login_required() decorator to ensure only those logged in can
# access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('app:index'))

def about(request):
    # prints out whether the method is a GET or a POST
    print(request.method)
    # prints out the user name, if no one is logged in it prints `AnonymousUser`
    context_dict = {}


    return render(request, 'app/about.html', context=context_dict)

def show_restaurants(request):
    # Define sorting options
    SORT_OPTIONS = {
        'name': 'Name (A-Z)',
        'rating': 'Rating (High to Low)',
        'cuisine': 'Cuisine (A-Z)',
    }

    cuisines = Cuisine.objects.all()

    FILTER_OPTIONS = {cuisine.name: cuisine.name for cuisine in cuisines}
    FILTER_OPTIONS['None'] = 'None'
    # Get query parameters for sorting and filtering
    sort_by = request.GET.get('sort', 'name')  # Default sort by name
    filter_only = request.GET.get('filter', None)
    city = request.GET.get('city', '').strip()

    # Filter restaurants by cuisine if a filter is applied
    restaurant_list = Restaurant.objects.all()

    if filter_only != 'None' and filter_only in FILTER_OPTIONS:
        print(filter_only)
        restaurant_list = restaurant_list.filter(cuisine__name=filter_only)


    # Sort restaurants based on the selected option
    if sort_by == 'rating':
        restaurant_list = sorted(restaurant_list, key=lambda r: r.calculate_average_stars(), reverse=True)
    elif sort_by == 'cuisine':
        restaurant_list = restaurant_list.order_by('cuisine__name')
    else:  # Default to sorting by name
        restaurant_list = restaurant_list.order_by('name')

    context_dict = {
        'restaurants': restaurant_list,
        'current_sort': sort_by,
        'current_filter': filter_only,
        'filter_options': FILTER_OPTIONS,
        'sort_options': SORT_OPTIONS,
    }

    return render(request, 'app/restaurants.html', context=context_dict)

@login_required
def manage_restaurant(request, restaurant_slug):
    restaurant = Restaurant.objects.get(slug=restaurant_slug)

    if not (Restaurant.objects.get(slug=restaurant_slug).manager == request.user or request.user.is_superuser):
        return HttpResponseForbidden("You are not authorized to access this page.")

    if request.method == 'POST':
        restaurant_form = RestaurantForm(request.POST, instance=restaurant)
        if restaurant_form.is_valid():
            restaurant_form.save()
            print(restaurant.slug)
            return redirect('app:manage_restaurant', restaurant_slug=restaurant.slug)
    else:
        restaurant_form = RestaurantForm(instance=restaurant)

    bookings = Booking.objects.filter(restaurant=restaurant)
    custom_hours = CustomHours.objects.filter(restaurant=restaurant)
    standard_hours = StandardHours.objects.filter(restaurant=restaurant)

    context = {
        'restaurant': restaurant,
        'bookings': bookings,
        'custom_hours': custom_hours,
        'standard_hours': standard_hours,
        'restaurant_form': restaurant_form,
    }

    return render(request, 'app/manage_restaurant.html', context)

# filepath: /Users/petervine/Developer/RestaBook/app/views.py
@login_required
def add_standard_hours(request, restaurant_slug):
    restaurant = get_object_or_404(Restaurant, slug=restaurant_slug)

    if not (restaurant.manager == request.user or request.user.is_superuser):
        return HttpResponseForbidden("You are not authorized to access this page.")

    # Check if editing an existing standard hour
    standard_hour_id = request.GET.get('edit') or request.POST.get('edit')
    if standard_hour_id:
        standard_hour = get_object_or_404(StandardHours, id=standard_hour_id)
    else:
        standard_hour = None

    if request.method == 'POST':
        form = StandardHoursForm(request.POST, instance=standard_hour)
        if form.is_valid():
            # Check for duplicate hours
            week_day = form.cleaned_data['week_day']
            if not standard_hour or standard_hour.week_day != week_day:
                duplicate_hours = StandardHours.objects.filter(
                    restaurant=restaurant, week_day=week_day
                ).exclude(id=standard_hour.id if standard_hour else None)

                if duplicate_hours.exists():
                    form.add_error('week_day', 'Standard hours for this day already exist.')
                else:
                    standard_hours = form.save(commit=False)
                    standard_hours.restaurant = restaurant
                    standard_hours.save()
                    return redirect('app:manage_restaurant', restaurant_slug=restaurant_slug)
            else:
                standard_hours = form.save(commit=False)
                standard_hours.restaurant = restaurant
                standard_hours.save()
                return redirect('app:manage_restaurant', restaurant_slug=restaurant_slug)
        else:
            print(form.errors)  # Debugging: Print form errors if invalid
    else:
        form = StandardHoursForm(instance=standard_hour)

    context = {
        'restaurant': restaurant,
        'form': form,
    }

    return render(request, 'app/add_standard_hours.html', context)

@login_required
def add_custom_hours(request, restaurant_slug):
    restaurant = get_object_or_404(Restaurant, slug=restaurant_slug)

    if not (restaurant.manager == request.user or request.user.is_superuser):
        return HttpResponseForbidden("You are not authorized to access this page.")

    # Check if editing an existing custom hour
    custom_hour_id = request.GET.get('edit') or request.POST.get('edit')
    if custom_hour_id:
        custom_hour = get_object_or_404(CustomHours, id=custom_hour_id, restaurant=restaurant)
    else:
        custom_hour = None

    if request.method == 'POST':
        form = CustomHoursForm(request.POST, instance=custom_hour)
        if form.is_valid():
            # Check for duplicate hours
            date = form.cleaned_data['date']
            if not custom_hour or custom_hour.date != date:
                if CustomHours.objects.filter(restaurant=restaurant, date=date).exists():
                    form.add_error('date', 'Custom hours for this date already exist.')
                else:
                    custom_hours = form.save(commit=False)
                    custom_hours.restaurant = restaurant
                    custom_hours.save()
                    return redirect('app:manage_restaurant', restaurant_slug=restaurant_slug)
            else:
                custom_hours = form.save(commit=False)
                custom_hours.restaurant = restaurant
                custom_hours.save()
                return redirect('app:manage_restaurant', restaurant_slug=restaurant_slug)
        else:
            print(form.errors)  # Debugging: Print form errors if invalid
    else:
        form = CustomHoursForm(instance=custom_hour)

    context = {
        'restaurant': restaurant,
        'form': form,
    }

    return render(request, 'app/add_custom_hours.html', context)

@login_required
def book_table(request, restaurant_slug):
    restaurant = get_object_or_404(Restaurant, slug=restaurant_slug)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if not restaurant.bookings_allowed:
            return HttpResponseForbidden("Bookings are not allowed for this restaurant.")

        if form.is_valid():
            booking_date = form.cleaned_data.get('date')
            booking_time = form.cleaned_data.get('time')

            # Validate booking date and time
            if booking_date and booking_time:
                # Check for custom hours on the booking date
                custom_hours = CustomHours.objects.filter(restaurant=restaurant, date=booking_date).first()
                if custom_hours:
                    if not custom_hours.bookings_allowed or not (custom_hours.opening_time <= booking_time < custom_hours.closing_time):
                        form.add_error(None, "The restaurant is closed at the selected time.")
                else:
                    # Check standard hours for the day of the week
                    day_of_week = booking_date.strftime('%A')
                    standard_hours = StandardHours.objects.filter(restaurant=restaurant, week_day=day_of_week).first()
                    if not standard_hours or not standard_hours.bookings_allowed or not (standard_hours.opening_time <= booking_time < standard_hours.closing_time):
                        form.add_error(None, "The restaurant is closed at the selected time.")
            else:
                form.add_error(None, "Please provide a valid date and time for the booking.")

            # If no errors were added, save the booking
            if not form.errors:
                booking = form.save(commit=False)
                booking.user = request.user
                booking.restaurant = restaurant
                booking.save()
                return redirect('app:show_restaurant', restaurant_slug=restaurant_slug)
        else:
            print(form.errors)  # Debugging: Print form errors if invalid
    else:
        form = BookingForm()

    context = {
        'restaurant': restaurant,
        'form': form,
    }

    return render(request, 'app/book_table.html', context)

def calculate_free_slots(hours, restaurant):
    """
    Calculate free slots for a given StandardHours or CustomHours object.
    """
    free_slots = []
    current_time = hours.opening_time
    while current_time < hours.closing_time:
        # Count existing bookings for this time slot
        bookings_count = Booking.objects.filter(
            restaurant=restaurant,
            date=datetime.date.today(),
            time=current_time
        ).count()

        # Calculate free tables
        free_tables = hours.number_tables - bookings_count
        free_slots.append({
            'time': current_time,
            'free_tables': free_tables
        })

        # Increment time by 30 minutes
        current_time = (datetime.datetime.combine(datetime.date.today(), current_time) +
                        datetime.timedelta(minutes=30)).time()

    return free_slots




class opening_times_object:
    def __init__(self, day_of_week, opening_time, closing_time):
        self.day_of_week = day_of_week
        self.opening_time = opening_time
        self.closing_time = closing_time


def show_restaurant(request, restaurant_slug):
    context_dict = {}
    try:
        restaurant = Restaurant.objects.get(slug=restaurant_slug)
        context_dict['restaurant'] = restaurant
        context_dict['name'] = restaurant.name
        context_dict['cuisine'] = restaurant.cuisine
        context_dict['email'] = restaurant.email
        context_dict['phone'] = restaurant.phone
        context_dict['address'] = restaurant.address


        # Fetch standard and custom hours
        standard_hours = StandardHours.objects.filter(restaurant=restaurant)
        custom_hours = CustomHours.objects.filter(restaurant=restaurant)

        # Calculate free bookings for each time slot

        opening_times = []
        today = datetime.date.today()

 
        for i in range(7):
            current_date = today + datetime.timedelta(days=i)
            current_day = current_date.strftime('%A')  # Get the day of the week (e.g., 'Monday')

            # Check if there are custom hours for the current date
            custom_hour = custom_hours.filter(date=current_date).first()
            if custom_hour:
                opening_times.append(opening_times_object(
                    day_of_week=current_date.strftime('%A'),
                    opening_time=custom_hour.opening_time,
                    closing_time=custom_hour.closing_time
                ))
            else:
                # Check if there are standard hours for the current day
                standard_hour = standard_hours.filter(week_day=current_day).first()
                if standard_hour:
                    opening_times.append(opening_times_object(
                        day_of_week=current_date.strftime('%A'),
                        opening_time=standard_hour.opening_time,
                        closing_time=standard_hour.closing_time
                    ))

        context_dict['opening_times'] = opening_times

        if restaurant.manager == request.user:
            context_dict['site_manager'] = True
        else:
            context_dict['site_manager'] = False



        context_dict['opening_times'] = opening_times

        if request.method == 'POST' and request.user.is_authenticated:
            if context_dict['site_manager']:
                return redirect('app:show_restaurant', restaurant_slug=restaurant_slug)
            


            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.restaurant = restaurant
                review.review_date = datetime.date.today()
                review.save()
                return redirect('app:show_restaurant', restaurant_slug=restaurant_slug)
        else:
            form = ReviewForm()


        context_dict['form'] = form
        all_reviews = Review.objects.filter(restaurant=restaurant).order_by('-review_date')
        paginator = Paginator(all_reviews, 3)
        page_number = request.GET.get('page')
        reviews_page = paginator.get_page(page_number)
        context_dict['reviews'] = reviews_page

    except Restaurant.DoesNotExist:
        pass

    return render(request, 'app/restaurant.html', context=context_dict)


@login_required
def user_profile(request):
    user = request.user

    avatar_form = AvatarUploadForm(instance=request.user)
    if request.method == 'POST':
        avatar_form = AvatarUploadForm(request.POST, request.FILES, instance=request.user)
        if avatar_form.is_valid():
            avatar_form.save()
            return redirect('app:profile')
    
    # Fetch bookings for the logged-in user
    user_bookings = Booking.objects.filter(user=user).order_by('-date', '-time')

    # Paging for bookings
    booking_paginator = Paginator(user_bookings, 5)
    booking_page_number = request.GET.get('booking_page')
    bookings = booking_paginator.get_page(booking_page_number)

    # Fetch reviews made by the logged-in user
    user_reviews = Review.objects.filter(user=user).order_by('-review_date')

    #paging for reviews
    review_paginator = Paginator(user_reviews, 3)
    review_page_number = request.GET.get('review_page')
    reviews = review_paginator.get_page(review_page_number)

    context = {
        'avatar_form': avatar_form,
        'user': user,
        'bookings': bookings,
        'reviews': reviews,
    }
    
    return render(request, 'app/profile.html', context)

def search_restaurants(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        results = Restaurant.objects.filter(name__icontains=query)

    recent_restaurants = None
    if request.user.is_authenticated:
        recent_restaurants = (
            Restaurant.objects
            .filter(booking__user=request.user)
            .distinct()
            .order_by('-booking__date')[:5]
        )

    return render(request, 'app/search.html', {
                        'query': query,
                        'results': results,
                        'recent_restaurants': recent_restaurants,
                  })

@login_required
def complete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == 'POST':
        booking.is_completed = True
        booking.save()

    return redirect('app:profile')

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == 'POST' and not booking.is_completed:
        booking.delete()
    
    return redirect('app:profile')
