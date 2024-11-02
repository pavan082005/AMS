from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from .models import Profile

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
