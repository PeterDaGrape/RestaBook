from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from app.forms import UserProfileForm, UserForm, RestaurantForm, StandardHoursForm, CustomHoursForm, BookingForm, ReviewForm
from app.models import Restaurant, Booking, CustomHours, Restaurant, StandardHours, Review, Cuisine
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


def register(request):
    # A boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves,
            # we set commit=False. This delays saving the model
            # until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user


            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to indicate that the template
            # registration was successful.
            registered = True
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(user_form.errors, profile_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()

        # Render the template depending on the context.
    return render(request, 'app/register.html', context = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


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

@login_required
def add_standard_hours(request, restaurant_slug):
    restaurant = get_object_or_404(Restaurant, slug=restaurant_slug)

    if not (Restaurant.objects.get(slug=restaurant_slug).manager == request.user or request.user.is_superuser):
        return HttpResponseForbidden("You are not authorized to access this page.")

    if request.method == 'POST':
        form = StandardHoursForm(request.POST)
        if form.is_valid():
            standard_hours = form.save(commit=False)
            standard_hours.restaurant = restaurant
            standard_hours.save()
            return redirect('app:manage_restaurant', restaurant_slug=restaurant_slug)
    else:
        form = StandardHoursForm()

    context = {
        'restaurant': restaurant,
        'form': form,
    }

    return render(request, 'app/add_standard_hours.html', context)

@login_required
def add_custom_hours(request, restaurant_slug):
    restaurant = get_object_or_404(Restaurant, slug=restaurant_slug)

    if not (Restaurant.objects.get(slug=restaurant_slug).manager == request.user or request.user.is_superuser):
        return HttpResponseForbidden("You are not authorized to access this page.")

    if request.method == 'POST':
        form = CustomHoursForm(request.POST)
        if form.is_valid():
            custom_hours = form.save(commit=False)
            custom_hours.restaurant = restaurant
            custom_hours.save()
            return redirect('app:manage_restaurant', restaurant_slug=restaurant_slug)
    else:
        form = CustomHoursForm()

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
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.restaurant = restaurant
            booking.save()
            return redirect('app:show_restaurant', restaurant_slug=restaurant_slug)
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





        context_dict['opening_times'] = opening_times

        if request.method == 'POST' and request.user.is_authenticated:
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
        context_dict['reviews'] = Review.objects.filter(restaurant=restaurant)
        if restaurant.manager == request.user:
            context_dict['site_manager'] = True
        else:
            context_dict['site_manager'] = False

    except Restaurant.DoesNotExist:
        pass

    return render(request, 'app/restaurant.html', context=context_dict)


@login_required
def user_profile(request):
    user = request.user

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
            return redirect('app:profile')  # Refresh page after update
    else:
        user_form = UserForm(instance=user)

    return render(request, 'app/profile.html', {'user_form': user_form})
