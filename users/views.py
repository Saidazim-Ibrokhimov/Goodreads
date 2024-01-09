from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout
from django.contrib.auth.models import User

from django.views import View
from .forms import UserCreateForm, UserUpdateForm, MessageForm 
from .models import Contact, CustomUser
from django.shortcuts import get_object_or_404


# Create your views here.

class RegisterView(View):
	def get(self, request):
		create_form = UserCreateForm()
		context = {
		'form':create_form
		}
		return render(request, "users/register.html", context)

	def post(self, request):
		create_form = UserCreateForm(data=request.POST)
		if create_form.is_valid():
			create_form.save()
			return redirect('users:login')
		else:
			context = {
			'form': create_form
			}
			return render(request, "users/register.html", context)

class LoginView(View):
	def get(self, request):
		login_form = AuthenticationForm()
		return render(request, 'users/login.html', {'login_form':login_form})

	def post(self, request):
		login_form = AuthenticationForm(data=request.POST)

		if login_form.is_valid():
			user = login_form.get_user()
			login(request, user)
			messages.success(request, "You have succesfully logged in!")

			return redirect(reverse('home_page'))
		else:
			return render(request, 'users/login.html', {'login_form':login_form})

class LogOutView(LoginRequiredMixin, View):
	def get(self, request):
		logout(request)
		messages.info(request, 'You have succesfully logged out!')
		return redirect('landing_page')


class ProfilePageView(LoginRequiredMixin, View):
	def get(self, request, username):
		user = get_object_or_404(CustomUser, username=username)

		return render(request, 'users/profile.html', {'user':user})

class ProfileUpdateView(LoginRequiredMixin, View):
	def get(self, request):
		user_update_form = UserUpdateForm(instance=request.user)
		return render(request, "users/profile_edit.html", {'form':user_update_form})

	def post(self, request):
		user_update_form = UserUpdateForm(
			instance=request.user, 
			data=request.POST,
			files=request.FILES
			)

		if user_update_form.is_valid():
			user_update_form.save()
			messages.success(request, "You have succesfully updated your profile")
			return redirect(reverse('users:profile_page', kwargs={'username':request.user.username}))
		else:
			return render(request, "users/profile_edit.html", {'form':user_update_form})

@login_required(login_url='users:login')
def contact_page(request):
	if request.method == 'GET':
		message_form = MessageForm()
		return render(request, 'contact.html', {'form':message_form})
	if request.method == 'POST':
		message_form = MessageForm(data=request.POST)
		if message_form.is_valid():
			Contact.objects.create(
				user=request.user,
				summary=message_form.cleaned_data['summary'],
				message=message_form.cleaned_data['message']
				)
			messages.success(request, 'Your message is sent to owner of the site!')
			return redirect(reverse('home_page'))
		return render(request, 'contact.html', {'form':message_form})
