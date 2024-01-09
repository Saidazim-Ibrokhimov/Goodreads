from django.urls import path
from .views import (
	RegisterView, 
	LoginView, 
	ProfilePageView, 
	LogOutView,
	ProfileUpdateView, 
	contact_page
)

app_name = 'users'

urlpatterns = [
	path('register/', RegisterView.as_view(), name='register'),
	path('login/', LoginView.as_view(), name='login'),
	path('logout/', LogOutView.as_view(), name='logout'),
	path('profile/<str:username>/', ProfilePageView.as_view(), name='profile_page'),
	path('profile-edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('contact/', contact_page, name='contact'),

]