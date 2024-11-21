from django.shortcuts import render, redirect, get_object_or_404, reverse
from .forms import SignUpForm, SignInForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from .models import User, Admin
from .forms import MenuItemForm
from .models import MenuItem, Cart, Order, Notification
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction


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

                # Check if the user is blocked
                if user.is_blocked:
                    form.add_error(None, 'Your account is blocked. Please contact amrutha@gmail.com for help.')
                else:

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

    orders = Order.objects.filter(user_id=user_id).order_by('-created_at')

    # Render the profile page with user details retrieved from the database
    context = {
        'fullname': user.fullname,
        'email': user.email,
        'orders': orders
    }
    return render(request, 'AmruthaRestaurant/customer_dashboard.html', context)


def logout(request):
    request.session.flush()  # Clear all session data to log out the user
    return redirect('signin')


def adminlogout(request):
    request.session.flush()  # Clear all session data to log out the user
    return redirect('adminsignin')


def customermenu(request):
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
            except Admin.DoesNotExist:
                form.add_error(None, 'Email or Password is Incorrect')

    else:
        form = SignInForm()

    return render(request, 'AmruthaRestaurant/admin_signin.html', {'form': form})


def admindashboard(request):
    # Check if the user is logged in by checking session data for 'user_id'
    user_id = request.session.get('user_id')

    if not user_id:
        # If no admin user is logged in, redirect to the sign-in page
        return redirect('adminsignin')

    # Retrieve all orders from the database
    orders = Order.objects.all().order_by('-created_at')

    # Render the admin dashboard page with order summaries
    context = {
        'orders': orders
    }
    return render(request, 'AmruthaRestaurant/admin_dashboard.html', context)


def customer_list(request):
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
    users = User.objects.all()  # Retrieve all users from the database
    return render(request, 'AmruthaRestaurant/customer_list.html', {'users': users})


def add_item(request):
    # Check if the user is logged in by checking session data for 'user_id'
    user_id = request.session.get('user_id')

    if not user_id:
        # If no user is logged in, redirect to the sign-in page
        return redirect('adminsignin')

    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('menu_items')  # Replace 'menu_items' with the URL name for the menu list view
    else:
        form = MenuItemForm()
    return render(request, 'AmruthaRestaurant/add_menu_item.html', {'form': form})


def menu_items(request):
    # Check if the user is logged in by checking session data for 'user_id'
    user_id = request.session.get('user_id')

    if not user_id:
        # If no user is logged in, redirect to the sign-in page
        return redirect('adminsignin')

    try:
        # Retrieve the user's information from the database based on the session's user_id
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        # Handle the case where the user doesn't exist in the database
        return redirect('adminsignin')

    menu_items = MenuItem.objects.all()
    edit_success = request.session.pop('edit_success', None)
    return render(request, 'AmruthaRestaurant/menu_items.html',
                  {'menu_items': menu_items, 'edit_success': edit_success})


def product_detail(request, product_id):
    # Check if the user is logged in by checking session data for 'user_id'
    user_id = request.session.get('user_id')

    if not user_id:
        # If no user is logged in, redirect to the sign-in page
        return redirect('signin')

    product = get_object_or_404(MenuItem, id=product_id)
    return render(request, 'AmruthaRestaurant/product_detail.html', {'product': product})


def add_to_cart(request, product_id):
    if request.method == 'POST':
        # Retrieve user ID from session
        user_id = request.session.get('user_id')

        # Check if the user is logged in by verifying if the user_id exists in session
        if user_id is None:
            return redirect('signin')  # Redirect to login if not logged in

        # Fetch the user from the database
        user = get_object_or_404(User, id=user_id)

        # Fetch product and calculate total price
        product = get_object_or_404(MenuItem, id=product_id)
        quantity = int(request.POST.get('quantity', 1))

        # Check if quantity can be safely converted to an integer and is non-negative
        try:
            quantity = int(quantity)
            if quantity < 0:
                quantity = 1  # Default to 1 if a negative value slips through
        except (TypeError, ValueError):
            quantity = 1  # Default to 1 if conversion fails

        # Log to verify the correct value
        print(f"Quantity received: {quantity}")

        total_price = quantity * product.price

        # Check if the product is already in the cart for the user
        cart_item, created = Cart.objects.get_or_create(user=user, product=product, quantity=quantity,
                                                        total_price=total_price)

        if not created:
            cart_item.quantity += quantity
            cart_item.total_price += total_price
        else:
            cart_item.quantity = quantity
            cart_item.total_price = total_price

        cart_item.save()
        messages.success(request, f"{product.name} has been added to your cart.")
        return redirect(reverse('product_detail', args=[product_id]))  # Redirect back to product page


def view_cart(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('signin')  # Redirect to sign-in if user is not logged in

    user = get_object_or_404(User, id=user_id)

    # Fetch only cart items with a "pending" status for the logged-in user
    cart_items = Cart.objects.filter(user=user, status='pending')

    # Calculate the total for all pending items in the cart
    total_price_all_products = sum(item.total_price for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price_all_products': total_price_all_products
    }
    return render(request, 'AmruthaRestaurant/cart.html', context)


def remove_cart_item(request, item_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('signin')

    cart_item = get_object_or_404(Cart, id=item_id, user_id=user_id)
    cart_item.delete()
    return redirect('cart')  # Replace 'cart' with the name of your cart URL


def checkout(request):
    # Check if the user is logged in
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('signin')  # Redirect to sign-in if user is not logged in

    # Retrieve the user's cart items
    cart_items = Cart.objects.filter(user_id=user_id, status='pending')

    # Calculate the total price for all items in the cart
    total_price_all_products = sum(item.total_price for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price_all_products': total_price_all_products,
    }

    return render(request, 'AmruthaRestaurant/checkout.html', context)


@transaction.atomic
def place_order(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('signin')

    user = User.objects.get(id=user_id)
    cart_items = Cart.objects.filter(user=user, status='pending')
    total_price_all_products = sum(item.total_price for item in cart_items)

    if request.method == 'POST':
        address_line1 = request.POST.get('address_line1')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        country = request.POST.get('country')
        payment_method = request.POST.get('payment_method')
        paypal_email = request.POST.get('paypal_email', None)
        special_instructions = request.POST.get('special_instructions', '')

        # Capture credit/debit card details if card payment is selected
        card_number = request.POST.get('card_number') if payment_method == 'card' else None
        card_expiry_date = request.POST.get('card_expiry_date') if payment_method == 'card' else None
        card_cvv = request.POST.get('card_cvv') if payment_method == 'card' else None

        # Capture digital wallet type if digital wallet is selected
        digital_wallet_type = request.POST.get('digital_wallet_type') if payment_method == 'digital_wallet' else None

        # Create and save the order
        order = Order.objects.create(
            user=user,
            address_line1=address_line1,
            city=city,
            state=state,
            zip_code=zip_code,
            country=country,
            payment_method=payment_method,
            paypal_email=paypal_email if payment_method == 'paypal' else None,
            card_number=card_number,
            card_expiry_date=card_expiry_date,
            card_cvv=card_cvv,
            digital_wallet_type=digital_wallet_type,
            special_instructions=special_instructions,
            total_price=total_price_all_products
        )

        order.cart_items.set(cart_items)  # Link cart items to the order
        cart_items.update(status='purchased')  # Mark cart items as purchased

        messages.success(request, f"You have placed your order successfully.")

        # Create a notification for the customer
        Notification.objects.create(
            order_number=order.order_number,
            user=user,
            notification=f"Your order #{order.order_number} has been placed successfully",
            read_status=False
        )

        return redirect('order_success')

    context = {
        'cart_items': cart_items,
        'total_price_all_products': total_price_all_products,
    }
    return render(request, 'AmruthaRestaurant/checkout.html', context)


def order_details(request, order_number):
    # Check if the user is logged in
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('signin')

    # Retrieve the specific order by order_number, ensuring it belongs to the logged-in user
    order = get_object_or_404(Order, order_number=order_number, user_id=user_id)

    # Pass the order details to the template
    context = {
        'order': order
    }
    return render(request, 'AmruthaRestaurant/order_details.html', context)


def order_success(request):
    return render(request, 'AmruthaRestaurant/order_success.html')


def admin_order_details(request, order_number):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('adminsignin')
    order = get_object_or_404(Order, order_number=order_number)
    context = {
        'order': order,

    }
    return render(request, 'AmruthaRestaurant/admin_order_details.html', context)


def admin_profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('adminsignin')

    # Retrieve the admin user details
    admin_user = get_object_or_404(Admin, id=user_id)

    return render(request, 'AmruthaRestaurant/admin_profile.html', {'admin_user': admin_user})


def customer_profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('signin')

    # Retrieve the admin user details
    customer = get_object_or_404(User, id=user_id)

    return render(request, 'AmruthaRestaurant/customer_profile.html', {'customer': customer})


def mark_order_processing(request, order_number):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('adminsignin')
    order = get_object_or_404(Order, order_number=order_number)
    order.status = 'processing'
    order.save()
    return redirect('admin_order_details', order_number=order_number)


def mark_order_delivered(request, order_number):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('adminsignin')
    order = get_object_or_404(Order, order_number=order_number)
    order.status = 'delivered'
    order.save()
    return redirect('admin_order_details', order_number=order_number)


def block_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_blocked = True
    user.save()

    return redirect('customer_list')  # Redirect to the admin dashboard or relevant page


def unblock_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_blocked = False
    user.save()

    return redirect('customer_list')  # Redirect to the admin dashboard or relevant page


def edit_item(request, item_id):
    # Check if the user is logged in by checking session data for 'user_id'
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('adminsignin')

    # Retrieve the item or return a 404 if not found
    item = get_object_or_404(MenuItem, id=item_id)

    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            # Set a session variable to indicate success
            messages.success(request, f"{item.name} has been edited successfully.")
            return redirect('menu_items')  # Redirect to the menu items page
    else:
        form = MenuItemForm(instance=item)

    return render(request, 'AmruthaRestaurant/edit_menu_item.html', {'form': form, 'item': item})


def delete_item(request, item_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('adminsignin')

    # Retrieve the item to be deleted
    item = get_object_or_404(MenuItem, id=item_id)

    item.delete()

    # Set a success message to indicate that the item was deleted
    messages.success(request, f'Item has been deleted successfully.')
    return redirect('menu_items')
def admin_notifications_view(request):
    # Ensure that only admins can access this view
    admin_id = request.session.get('user_id')
    if not admin_id:
        return redirect('adminsignin')
        # Check if a specific notification is being clicked to mark it as read
    notification_id = request.GET.get('notification_id')
    if notification_id:
        try:
            notification = Notification.objects.get(id=notification_id)
            if not notification.read_status:
                notification.read_status = True
                notification.save()
        except Notification.DoesNotExist:
            pass  # Notification not found, proceed to display all notifications

    # Fetch all notifications, ordered by creation time
    notifications = Notification.objects.all().order_by('-created_at')
    # Count unread notifications


    return render(request, 'AmruthaRestaurant/admin_notifications.html', {'notifications': notifications})
def customer_notifications_view(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, id=user_id)

    notification_id = request.GET.get('notification_id')
    if notification_id:
        try:
            notification = Notification.objects.get(id=notification_id)
            if not notification.customer_read_status:
                notification.customer_read_status = True
                notification.save()
        except Notification.DoesNotExist:
            pass  # Notification not found, proceed to display all notifications

    # Fetch notifications for the logged-in user
    notifications = Notification.objects.filter(user=user).order_by('-created_at')


    return render(request, 'AmruthaRestaurant/customer_notifications.html', {'notifications': notifications})