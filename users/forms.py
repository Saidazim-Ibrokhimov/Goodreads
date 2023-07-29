from django import forms
from users.models import CustomUser, Contact
from django.core.mail import send_mail

class UserCreateForm(forms.ModelForm):
	class Meta:
		model = CustomUser
		fields = ('username', 'first_name', 'last_name', 'email', 'password',)
	
	def save(self, commit=True):
		user = super().save(commit)
		user.set_password(self.cleaned_data['password'])
		user.save()

		# if user.email:
		# 	send_mail(
		# 		'Welcome to Goodreads clone',
		# 		'Hi, {user.username}.Welcome to Goodreads colne. Enjoy the books and reviews',
		# 		'saidazimboy2@gmail.com',
		# 		[user.email]


		# 		)
		return user

class UserUpdateForm(forms.ModelForm):
	class Meta:
		model = CustomUser 
		fields = ['username', 'first_name', 'last_name', 'email', 'profile_picture']

class MessageForm(forms.ModelForm):
	class Meta:
		model = Contact
		fields = ('summary', 'message',)