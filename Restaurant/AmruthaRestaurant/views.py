from django.shortcuts import render, redirect
from .forms import SignUpForm, SignInForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from .models import User, Admin
from .forms import MenuItemForm
from .models import MenuItem
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'AmruthaRestaurant/index.html')


def about(request):
    return render(request, 'AmruthaRestaurant/about.html')


def foodmenu(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'AmruthaRestaurant/menu.html', {'menu_items': menu_items})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Process the form data
            fullname = form.cleaned_data['fullname']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            copassword = form.cleaned_data['copassword']

            if password == copassword:
                hashed_password = make_password(password)  # Hash the password
                User.objects.create(
                    fullname=fullname,
                    email=email,
                    password=hashed_password
                )
                return redirect('signin')
            else:
                form.add_error(None, 'Passwords do not match')
    else:
        form = SignUpForm()

    return render(request, 'AmruthaRestaurant/register.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                # Try to fetch the user with the provided email
                user = User.objects.get(email=email)

                # Check if the provided password matches the stored hashed password
                if check_password(password, user.password):
                    # Log the user in (store user details in session)
                    request.session['user_id'] = user.id

                    return redirect('customerdashboard')  # Redirect to dashboard or success page
                else:
                    form.add_error(None, 'Email or Password is Incorrect')
            except User.DoesNotExist:
                form.add_error(None, 'Email or Password is Incorrect')

    else:
        form = SignInForm()

    return render(request, 'AmruthaRestaurant/signin.html', {'form': form})


def customerdashboard(request):
    # Check if the user is logged in by checking session data for 'user_id'
    user_id = request.session.get('user_id')

    if not user_id:
        # If no user is logged in, redirect to the sign-in page
        return redirect('signin')

    try:
        # Retrieve the user's information from the database based on the session's user_id
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        # Handle the case where the user doesn't exist in the database
        return redirect('signin')

    # Render the profile page with user details retrieved from the database
    context = {
        'fullname': user.fullname,
        'email': user.email
    }
    return render(request, 'AmruthaRestaurant/customer_dashboard.html', context)


def logout(request):
    request.session.flush()  # Clear all session data to log out the user
    return redirect('signin')


def customermenu(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'AmruthaRestaurant/customer_menu.html', {'menu_items': menu_items})



def adminsignin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                # Try to fetch the user with the provided email
                user = Admin.objects.get(email=email)

                # Check if the provided password matches the stored hashed password
                if check_password(password, user.password):
                    # Log the user in (store user details in session)
                    request.session['user_id'] = user.id

                    return redirect('admindashboard')  # Redirect to dashboard or success page
                else:
                    form.add_error(None, 'Email or Password is Incorrect')
            except User.DoesNotExist:
                form.add_error(None, 'Email or Password is Incorrect')

    else:
        form = SignInForm()

    return render(request, 'AmruthaRestaurant/admin_signin.html', {'form': form})


def admindashboard(request):
    # Check if the user is logged in by checking session data for 'user_id'
    user_id = request.session.get('user_id')

    if not user_id:
        # If no user is logged in, redirect to the sign-in page
        return redirect('signin')

    try:
        # Retrieve the user's information from the database based on the session's user_id
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        # Handle the case where the user doesn't exist in the database
        return redirect('adminsignin')

    # Render the profile page with user details retrieved from the database
    context = {
        'fullname': user.fullname,
        'email': user.email
    }
    return render(request, 'AmruthaRestaurant/admin_dashboard.html', context)


def customer_list(request):
    users = User.objects.all()  # Retrieve all users from the database
    return render(request, 'AmruthaRestaurant/customer_list.html', {'users': users})


def add_item(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('menu_items')  # Replace 'menu_items' with the URL name for the menu list view
    else:
        form = MenuItemForm()
    return render(request, 'AmruthaRestaurant/add_menu_item.html', {'form': form})


def menu_items(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'AmruthaRestaurant/menu_items.html', {'menu_items': menu_items})
