from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rooms.models import Room
from .models import ChatRoom, Message
import json


@login_required
def chat_list(request):
    """Display all chat rooms for the current user"""
    user_chats = ChatRoom.objects.filter(participants=request.user).prefetch_related('participants', 'messages')
    
    # Add additional context for each chat
    chat_data = []
    total_unread = 0
    
    for chat in user_chats:
        other_participant = chat.get_other_participant(request.user)
        # Count unread messages from other participants
        unread_count = chat.messages.filter(
            is_read=False
        ).exclude(sender=request.user).count()
        
        total_unread += unread_count
        
        chat_data.append({
            'chat': chat,
            'other_participant': other_participant,
            'room': chat.room,
            'last_message': chat.last_message,
            'unread_count': unread_count,
        })
    
    return render(request, 'chat/chat_list.html', {
        'chats': chat_data,
        'total_unread': total_unread
    })


@login_required
def start_chat_with_owner(request, room_id):
    """Start or continue a chat with the room owner"""
    room = get_object_or_404(Room, id=room_id)
    
    # Prevent users from chatting with themselves
    if room.owner == request.user:
        messages.error(request, "You cannot message yourself about your own property.")
        return redirect('rooms:room_detail', pk=room_id)
    
    # Get or create the chat room
    chat_room, created = ChatRoom.objects.get_or_create(room=room)
    
    # Add participants if they're not already in the chat
    if not chat_room.participants.filter(id=request.user.id).exists():
        chat_room.participants.add(request.user)
    if not chat_room.participants.filter(id=room.owner.id).exists():
        chat_room.participants.add(room.owner)
    
    # Get all messages in this chat room
    messages_list = Message.objects.filter(chat_room=chat_room).select_related('sender')
    
    # Mark messages as read for the current user
    Message.objects.filter(
        chat_room=chat_room,
        is_read=False
    ).exclude(sender=request.user).update(is_read=True)
    
    return render(request, 'chat/chat_room.html', {
        'chat_room': chat_room,
        'room': room,
        'owner': room.owner,
        'messages': messages_list,
        'other_participant': room.owner if request.user != room.owner else chat_room.get_other_participant(request.user)
    })


@login_required
def chat_room(request, chat_room_id):
    """Access a specific chat room (for both owners and seekers)"""
    chat_room = get_object_or_404(ChatRoom, id=chat_room_id)
    
    # Verify user is a participant in this chat room
    if not chat_room.participants.filter(id=request.user.id).exists():
        messages.error(request, "You don't have access to this chat room.")
        return redirect('chat:chat_list')
    
    # Get all messages in this chat room
    messages_list = Message.objects.filter(chat_room=chat_room).select_related('sender')
    
    # Mark messages as read for the current user
    Message.objects.filter(
        chat_room=chat_room,
        is_read=False
    ).exclude(sender=request.user).update(is_read=True)
    
    # Determine other participant
    other_participant = chat_room.get_other_participant(request.user)
    
    return render(request, 'chat/chat_room.html', {
        'chat_room': chat_room,
        'room': chat_room.room,
        'owner': chat_room.room.owner,
        'messages': messages_list,
        'other_participant': other_participant
    })


@login_required
@require_POST
def send_message(request):
    """Send a message in a chat room (AJAX endpoint)"""
    try:
        # Get data from POST request
        chat_room_id = request.POST.get('chat_room_id')
        content = request.POST.get('content', '').strip()
        
        if not content:
            return JsonResponse({'success': False, 'error': 'Message cannot be empty'})
        
        # Get the chat room and verify user is a participant
        chat_room = get_object_or_404(ChatRoom, id=chat_room_id)
        
        if not chat_room.participants.filter(id=request.user.id).exists():
            return JsonResponse({'success': False, 'error': 'You are not a participant in this chat'})
        
        # Create the message
        message = Message.objects.create(
            chat_room=chat_room,
            sender=request.user,
            content=content
        )
        
        # Update chat room timestamp
        chat_room.save()  # This will update the updated_at field
        
        # Return success response with message data
        return JsonResponse({
            'success': True,
            'message': {
                'id': message.id,
                'content': message.content,
                'sender_name': message.sender.get_full_name() or message.sender.username,
                'timestamp': message.timestamp.strftime('%H:%M'),
                'is_own_message': message.sender == request.user
            }
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def get_chat_messages(request, chat_room_id):
    """Get messages for a chat room (AJAX endpoint for real-time updates)"""
    chat_room = get_object_or_404(ChatRoom, id=chat_room_id)
    
    # Verify user is a participant
    if not chat_room.participants.filter(id=request.user.id).exists():
        return JsonResponse({'success': False, 'error': 'Access denied'})
    
    # Get messages since a certain time (for real-time updates)
    since = request.GET.get('since')
    messages_qs = Message.objects.filter(chat_room=chat_room).select_related('sender')
    
    if since:
        try:
            from datetime import datetime
            since_datetime = datetime.fromisoformat(since)
            messages_qs = messages_qs.filter(timestamp__gt=since_datetime)
        except:
            pass
    
    messages_data = [{
        'id': msg.id,
        'content': msg.content,
        'sender_name': msg.sender.get_full_name() or msg.sender.username,
        'timestamp': msg.timestamp.isoformat(),
        'display_time': msg.timestamp.strftime('%H:%M'),
        'is_own_message': msg.sender == request.user
    } for msg in messages_qs]
    
    return JsonResponse({'success': True, 'messages': messages_data})


@login_required
def get_unread_count(request):
    """Get total unread message count for current user (AJAX endpoint)"""
    user_chats = ChatRoom.objects.filter(participants=request.user)
    total_unread = 0
    
    for chat in user_chats:
        unread_count = chat.messages.filter(
            is_read=False
        ).exclude(sender=request.user).count()
        total_unread += unread_count
    
    return JsonResponse({'unread_count': total_unread})


def debug_chat(request):
    """Debug page to show chat status"""
    return render(request, 'chat/debug_chat.html')
