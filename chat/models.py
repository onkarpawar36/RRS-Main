from django.db import models
from django.contrib.auth.models import User
from rooms.models import Room


class ChatRoom(models.Model):
    """A chat room between a user and a room owner"""
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='chats')
    participants = models.ManyToManyField(User, related_name='chat_rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('room',)
        ordering = ['-updated_at']

    def __str__(self):
        return f"Chat for {self.room.title}"

    def get_other_participant(self, user):
        """Get the other participant in the chat (not the current user)"""
        return self.participants.exclude(id=user.id).first()

    @property
    def last_message(self):
        """Get the last message in this chat room"""
        return self.messages.last()


class Message(models.Model):
    """A message in a chat room"""
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"
