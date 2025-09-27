from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.db import models
from .forms import UserSignUpForm, ProfileForm, UserUpdateForm
from .models import Profile


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('rooms:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context


def signup_view(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! Profile created automatically.')
            # Profile is created automatically by signals.py
            login(request, user)
            return redirect('accounts:profile_create')
    else:
        form = UserSignUpForm()
    
    return render(request, 'accounts/signup.html', {
        'form': form,
        'title': 'Sign Up'
    })


@login_required
def profile_create_view(request):
    try:
        profile = request.user.profile
        return redirect('accounts:profile_detail', user_id=request.user.id)
    except Profile.DoesNotExist:
        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                messages.success(request, 'Profile created successfully!')
                return redirect('accounts:profile_detail', user_id=request.user.id)
        else:
            form = ProfileForm()
    
    return render(request, 'accounts/profile_create.html', {
        'form': form,
        'title': 'Create Profile'
    })


@login_required
def profile_detail_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        if user == request.user:
            return redirect('accounts:profile_create')
        messages.error(request, 'Profile not found.')
        return redirect('rooms:home')
    
    # Get user's rooms (using dynamic import to avoid circular imports)
    from django.apps import apps
    Room = apps.get_model('rooms', 'Room')
    RoomReview = apps.get_model('rooms', 'RoomReview')
    
    user_rooms = Room.objects.filter(owner=user, is_available=True).order_by('-created_at')[:6]
    total_rooms = Room.objects.filter(owner=user).count()
    
    # Get user's reviews/ratings (if any)
    reviews = RoomReview.objects.filter(room__owner=user)
    avg_rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
    
    return render(request, 'accounts/profile_detail.html', {
        'profile': profile,
        'user_obj': user,
        'user_rooms': user_rooms,
        'total_rooms': total_rooms,
        'avg_rating': avg_rating or 0,
        'title': f"{profile.get_full_name}'s Profile"
    })


@login_required
def profile_edit_view(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        return redirect('accounts:profile_create')
    
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserUpdateForm(request.POST, instance=request.user)
        
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('accounts:profile_detail', user_id=request.user.id)
    else:
        profile_form = ProfileForm(instance=profile)
        user_form = UserUpdateForm(instance=request.user)
    
    return render(request, 'accounts/profile_edit.html', {
        'profile_form': profile_form,
        'user_form': user_form,
        'title': 'Edit Profile'
    })


def profile_list_view(request):
    """View to show all user profiles"""
    profiles = Profile.objects.all().order_by('-created_at')
    return render(request, 'accounts/profile_list.html', {
        'profiles': profiles,
        'title': 'All Users'
    })
