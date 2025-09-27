from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='accounts:login'), name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/create/', views.profile_create_view, name='profile_create'),
    path('profile/<int:user_id>/', views.profile_detail_view, name='profile_detail'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('profiles/', views.profile_list_view, name='profile_list'),
]