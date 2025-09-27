from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Room, RoomImage, RoomBookmark, RoomReview, RoomReport
from .forms import RoomForm, RoomImageFormSet, RoomReviewForm, RoomSearchForm, RoomReportForm


def home_view(request):
    """Home page with featured rooms"""
    featured_rooms = Room.objects.filter(featured=True, is_available=True)[:6]
    recent_rooms = Room.objects.filter(is_available=True).order_by('-created_at')[:8]
    
    # Get some statistics
    total_rooms = Room.objects.filter(is_available=True).count()
    total_cities = Room.objects.values('city').distinct().count()
    
    context = {
        'featured_rooms': featured_rooms,
        'recent_rooms': recent_rooms,
        'total_rooms': total_rooms,
        'total_cities': total_cities,
        'title': 'Find Your Perfect Rental Space'
    }
    return render(request, 'rooms/home.html', context)


def room_list_view(request):
    """List all rooms with search and filtering"""
    rooms = Room.objects.filter(is_available=True).select_related('owner').prefetch_related('images')
    
    # Handle search
    search = request.GET.get('search')
    if search:
        rooms = rooms.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(city__icontains=search) |
            Q(address__icontains=search)
        )
    
    # Handle category filter
    category = request.GET.get('category')
    if category:
        rooms = rooms.filter(category=category)
    
    # Handle room type filter
    room_type = request.GET.get('room_type')
    if room_type:
        rooms = rooms.filter(room_type=room_type)
    
    # Handle max price filter (from template)
    max_price = request.GET.get('max_price')
    if max_price:
        try:
            rooms = rooms.filter(price__lte=int(max_price))
        except ValueError:
            pass
    
    # Handle amenity filters
    if request.GET.get('wifi'):
        rooms = rooms.filter(wifi=True)
    if request.GET.get('parking'):
        rooms = rooms.filter(parking=True)
    if request.GET.get('ac'):
        rooms = rooms.filter(ac=True)
    if request.GET.get('laundry'):
        rooms = rooms.filter(laundry=True)
    if request.GET.get('food'):
        rooms = rooms.filter(food_included=True)
    if request.GET.get('gym'):
        rooms = rooms.filter(gym=True)
    
    # Handle sorting
    sort_by = request.GET.get('sort')
    if sort_by == 'price_low':
        rooms = rooms.order_by('price')
    elif sort_by == 'price_high':
        rooms = rooms.order_by('-price')
    elif sort_by == 'newest':
        rooms = rooms.order_by('-created_at')
    else:
        rooms = rooms.order_by('-created_at')  # default sorting
    
    # Pagination
    paginator = Paginator(rooms, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get user's bookmarked rooms for efficient checking
    user_bookmarked_rooms = set()
    if request.user.is_authenticated:
        user_bookmarked_rooms = set(
            RoomBookmark.objects.filter(user=request.user).values_list('room_id', flat=True)
        )
    
    # Get total count for display
    total_rooms = Room.objects.filter(is_available=True).count()
    
    context = {
        'page_obj': page_obj,
        'rooms': page_obj.object_list,
        'user_bookmarked_rooms': user_bookmarked_rooms,
        'total_rooms': total_rooms,
        'title': 'Browse Rooms'
    }
    return render(request, 'rooms/room_list.html', context)


def room_detail_view(request, pk):
    """Detailed view of a room"""
    room = get_object_or_404(Room, pk=pk, is_available=True)
    reviews = room.reviews.all()
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    
    # Check if user has bookmarked this room
    is_bookmarked = False
    if request.user.is_authenticated:
        is_bookmarked = RoomBookmark.objects.filter(user=request.user, room=room).exists()
    
    # Review form
    review_form = None
    if request.user.is_authenticated and request.user != room.owner:
        # Check if user has already reviewed
        user_review = reviews.filter(user=request.user).first()
        if not user_review:
            review_form = RoomReviewForm()
    
    # Handle review submission
    if request.method == 'POST' and review_form:
        review_form = RoomReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.room = room
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted!')
            return redirect('rooms:room_detail', pk=room.pk)
    
    # Similar rooms
    similar_rooms = Room.objects.filter(
        category=room.category,
        city=room.city,
        is_available=True
    ).exclude(pk=room.pk)[:4]
    
    context = {
        'room': room,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'is_bookmarked': is_bookmarked,
        'review_form': review_form,
        'similar_rooms': similar_rooms,
        'title': room.title
    }
    return render(request, 'rooms/room_detail.html', context)


@login_required
def room_create_view(request):
    """Create a new room"""
    if request.method == 'POST':
        form = RoomForm(request.POST)
        image_formset = RoomImageFormSet(request.POST, request.FILES)
        
        if form.is_valid() and image_formset.is_valid():
            room = form.save(commit=False)
            room.owner = request.user
            room.save()
            
            # Save image formset with proper validation
            try:
                image_formset.instance = room
                
                # Only save forms that are valid and have cleaned_data
                for image_form in image_formset.forms:
                    if image_form.is_valid() and hasattr(image_form, 'cleaned_data'):
                        if image_form.cleaned_data.get('image') and not image_form.cleaned_data.get('DELETE', False):
                            image_instance = image_form.save(commit=False)
                            image_instance.room = room
                            image_instance.save()
                            
            except Exception as e:
                print(f"Image formset save error: {e}")  # For debugging
            
            messages.success(request, 'Room created successfully!')
            return redirect('rooms:room_detail', pk=room.pk)
        else:
            # Add debug messages to see validation errors
            if not form.is_valid():
                messages.error(request, f'Form validation failed: {form.errors}')
            if not image_formset.is_valid():
                messages.error(request, f'Image formset validation failed: {image_formset.errors}')
    else:
        form = RoomForm()
        image_formset = RoomImageFormSet()
    
    context = {
        'form': form,
        'image_formset': image_formset,
        'title': 'Add New Room'
    }
    return render(request, 'rooms/room_create.html', context)


@login_required
def room_edit_view(request, pk):
    """Edit an existing room"""
    room = get_object_or_404(Room, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        image_formset = RoomImageFormSet(request.POST, request.FILES, instance=room)
        
        if form.is_valid():
            # Save the room first
            room_instance = form.save()
            
            # Try to save image formset, but don't block if it has validation issues with empty forms
            try:
                # Filter out empty forms before saving
                valid_forms = []
                for image_form in image_formset.forms:
                    # Check if form is valid AND has cleaned_data before accessing it
                    if image_form.is_valid() and hasattr(image_form, 'cleaned_data'):
                        if image_form.cleaned_data.get('image') or image_form.instance.pk:
                            valid_forms.append(image_form)
                
                # Save only the valid image forms
                for image_form in valid_forms:
                    # Double check cleaned_data exists before accessing DELETE
                    if hasattr(image_form, 'cleaned_data') and not image_form.cleaned_data.get('DELETE', False):
                        image_instance = image_form.save(commit=False)
                        image_instance.room = room_instance
                        image_instance.save()
                
                # Handle deletions - only process forms that have cleaned_data
                for image_form in image_formset.deleted_forms:
                    if image_form.instance.pk and hasattr(image_form, 'cleaned_data'):
                        image_form.instance.delete()
                        
            except Exception as e:
                # If image formset has issues, just ignore them since images are optional
                print(f"Image formset error: {e}")  # For debugging
                pass
            
            messages.success(request, 'Room updated successfully!')
            return redirect('rooms:room_detail', pk=room.pk)
        else:
            # Only show room form validation errors
            messages.error(request, f'Form validation failed: {form.errors}')
    else:
        form = RoomForm(instance=room)
        image_formset = RoomImageFormSet(instance=room)
    
    context = {
        'form': form,
        'image_formset': image_formset,
        'room': room,
        'title': f'Edit {room.title}'
    }
    return render(request, 'rooms/room_edit.html', context)


@login_required
def room_delete_view(request, pk):
    """Delete a room"""
    room = get_object_or_404(Room, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        try:
            # Get room title before deletion
            room_title = room.title
            
            # Delete the room (this will cascade delete related objects)
            room.delete()
            
            messages.success(request, f'Room "{room_title}" has been permanently deleted!')
            return redirect('rooms:my_rooms')
        except Exception as e:
            messages.error(request, f'Error deleting room: {str(e)}')
            return redirect('rooms:room_detail', pk=pk)
    
    # Get statistics for the confirmation page
    image_count = room.images.count()
    
    # Get related data counts safely using Django's app registry
    try:
        from django.apps import apps
        ChatRoom = apps.get_model('chat', 'ChatRoom')
        chat_count = ChatRoom.objects.filter(room=room).count()
    except (ImportError, LookupError):
        chat_count = 0
        
    bookmark_count = RoomBookmark.objects.filter(room=room).count()
    
    context = {
        'room': room,
        'image_count': image_count,
        'chat_count': chat_count,
        'bookmark_count': bookmark_count,
        'title': f'Delete {room.title}'
    }
    return render(request, 'rooms/room_delete.html', context)


@login_required
def my_rooms_view(request):
    """User's own rooms"""
    rooms = Room.objects.filter(owner=request.user).order_by('-created_at')
    featured_count = rooms.filter(featured=True).count()
    
    paginator = Paginator(rooms, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'rooms': page_obj.object_list,
        'featured_count': featured_count,
        'title': 'My Rooms'
    }
    return render(request, 'rooms/my_rooms.html', context)


@login_required
def bookmark_toggle(request, pk):
    """Toggle bookmark for a room"""
    if request.method == 'POST':
        try:
            room = get_object_or_404(Room, pk=pk)
            bookmark, created = RoomBookmark.objects.get_or_create(
                user=request.user,
                room=room
            )
            
            if not created:
                bookmark.delete()
                bookmarked = False
            else:
                bookmarked = True
            
            return JsonResponse({
                'bookmarked': bookmarked,
                'message': 'Added to bookmarks' if bookmarked else 'Removed from bookmarks'
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@login_required
def bookmarked_rooms_view(request):
    """User's bookmarked rooms"""
    bookmarks = RoomBookmark.objects.filter(user=request.user).select_related('room')
    rooms = [bookmark.room for bookmark in bookmarks]
    
    paginator = Paginator(rooms, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'rooms': page_obj.object_list,
        'title': 'Bookmarked Rooms'
    }
    return render(request, 'rooms/bookmarked_rooms.html', context)


@login_required
def report_room_view(request, pk):
    """Report a room for inappropriate content or issues"""
    room = get_object_or_404(Room, pk=pk)
    
    # Check if user has already reported this room
    existing_report = RoomReport.objects.filter(room=room, reporter=request.user).first()
    
    if request.method == 'POST':
        if existing_report:
            return JsonResponse({
                'success': False, 
                'error': 'You have already reported this room. Our team will review it soon.'
            })
        
        form = RoomReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.room = room
            report.reporter = request.user
            report.save()
            
            return JsonResponse({
                'success': True, 
                'message': 'Thank you for your report. Our team will review it within 24 hours.'
            })
        else:
            return JsonResponse({
                'success': False, 
                'error': 'Please correct the errors in the form.',
                'form_errors': form.errors
            })
    
    # For GET requests, return the form (though this will be handled via AJAX)
    form = RoomReportForm()
    
    context = {
        'room': room,
        'form': form,
        'existing_report': existing_report
    }
    
    return JsonResponse({
        'success': True,
        'has_reported': bool(existing_report)
    })
