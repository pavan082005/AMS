from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from .models import Item, Profile

def home(request):
    """Render the home page."""
    return render(request, 'unitrader/home.html')

def signup(request):
    """Handle user signup."""
    user_form = UserRegisterForm()
    profile_form = ProfileUpdateForm()
    
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileUpdateForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()  # Save the user data
            Profile.objects.create(user=user, **profile_form.cleaned_data)  # Create the profile
            username = user_form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('signin')  # Redirect to signin after successful signup
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'unitrader/signup.html', context)

def signin(request):
    """Handle user sign in."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect('home')  # Redirect to home page after sign in
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'unitrader/signin.html')

@login_required
def profile(request):
    """Display user profile."""
    profile = request.user.profile  # Fetch the profile associated with the logged-in user
    context = {
        'profile': profile,
    }
    return render(request, 'unitrader/profile.html', context)


@login_required
def edit_profile(request):
    """Allow user to edit their profile."""
    user_form = UserUpdateForm(instance=request.user)
    profile_form = ProfileUpdateForm(instance=request.user.profile)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()  # Save the user data
            profile_form.save()  # Save the profile data
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')  # Redirect to the profile page after saving changes

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'unitrader/edit_profile.html', context)


def custom_logout(request):
    """Log out the user."""
    logout(request)  # Log out the user
    messages.success(request, 'You have been logged out.')
    return redirect('signin')  # Redirect to the sign-in page after logout

def sell_item(request):
    if request.method == "POST":
        item_title = request.POST.get('item_title')
        item_description = request.POST.get('item_description')
        item_tags = request.POST.get('item_tags')
        item_age = request.POST.get('item_age')
        base_price = request.POST.get('base_price')
        quantity = request.POST.get('quantity')
        item_image = request.FILES.get('item_image')  # Access uploaded image

        # Create a new item instance
        item = Item(
            item_title=item_title,
            item_description=item_description,
            item_tags=item_tags,
            item_age=item_age,
            base_price=base_price,
            quantity=quantity,
            item_image=item_image,  # Save the uploaded image
            seller=request.user  # Associate with the logged-in user
        )
        item.save()  # Save the new item to the database

        # Redirect to the item list (buy_items) view
        return redirect('buy_items')

    return render(request, 'unitrader/sell_item.html')



def buy_items(request):
    available_items = Item.objects.filter(status='available')  # Only display available items
    return render(request, 'unitrader/buy_items.html', {'items': available_items})

@login_required
def buy_now(request, item_id):
    """Handle the 'Buy Now' option for LBin items."""
    item = get_object_or_404(Item, id=item_id)

    if item.item_tags != 'lbin' and item.status == 'available':
        # Render the confirmation page with item details
        context = {
            'item': item
        }
        return render(request, 'unitrader/confirm_purchase.html', context)

    return redirect('buy_items')


@login_required
def bid_on_item(request, item_id):
    """Handle placing a bid on an auction item."""
    item = get_object_or_404(Item, id=item_id)

    if request.method == "POST":
        bid_amount = request.POST.get('bid_amount')

        if bid_amount and float(bid_amount) > item.highest_bid:
            item.highest_bid = float(bid_amount)
            item.highest_bidder = request.user  
            item.save()
            messages.success(request, "Your bid has been placed successfully!")
        else:
            messages.error(request, "Your bid must be higher than the current highest bid.")

    return redirect('buy_items')  

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message
from .forms import MessageForm
from django.contrib.auth.models import User
from django.db.models import Q

@login_required
def chat_with_seller(request, seller_id):  # Make sure seller_id is included here
    seller = get_object_or_404(User, id=seller_id)
    
    # Retrieve messages between the buyer and the seller
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(recipient=seller)) |
        (Q(sender=seller) & Q(recipient=request.user))
    ).order_by('timestamp')

    if request.method == "POST":
        content = request.POST.get('message')
        if content:
            Message.objects.create(
                sender=request.user,
                recipient=seller,
                content=content
            )
            return redirect('chat_with_seller', seller_id=seller.id)  # Redirecting to the same view

    return render(request, 'unitrader/chat.html', {
        'seller': seller,
        'messages': messages
    })

def inbox(request):
    # Retrieve all messages for the logged-in user
    messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')

    for message in messages:
        message.is_read = True  # Mark message as read
        message.save()

    return render(request, 'unitrader/inbox.html', {
        'messages': messages,
    })
    

@login_required
def confirm_purchase(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == "POST":
        # Check if the user has enough coins
        if profile.coins >= item.base_price:
            profile.coins -= item.base_price  # Deduct the item's price
            item.quantity -= 1  # Reduce item quantity
            
            if item.quantity == 0:
                item.status = 'sold'
            
            # Save the updated profiles and items
            profile.save()
            item.save()
            
            messages.success(request, "Purchase confirmed! Coins deducted.")
            return redirect('buy_items')  # Redirect to buy_items or a success page
        else:
            messages.error(request, "You do not have enough coins to purchase this item.")
            return redirect('confirm_purchase', item_id=item_id)

    return render(request, 'unitrader/confirm_purchase.html', {'item': item})
