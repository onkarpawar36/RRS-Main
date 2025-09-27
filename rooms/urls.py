from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("rooms/", views.room_list_view, name="room_list"),
    path("room/<int:pk>/", views.room_detail_view, name="room_detail"),
    path("room/create/", views.room_create_view, name="room_create"),
    path("room/<int:pk>/edit/", views.room_edit_view, name="room_edit"),
    path("room/<int:pk>/delete/", views.room_delete_view, name="room_delete"),
    path("my-rooms/", views.my_rooms_view, name="my_rooms"),
    path("bookmarked-rooms/", views.bookmarked_rooms_view, name="bookmarked_rooms"),
    path("room/<int:pk>/bookmark/", views.bookmark_toggle, name="bookmark_toggle"),
    path("room/<int:pk>/report/", views.report_room_view, name="report_room"),
]
