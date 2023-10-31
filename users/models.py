from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
	profile_picture = models.ImageField(default='default_profile_pic.jpg', upload_to='users/profile-image/')

class Contact(models.Model):
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	summary = models.CharField(max_length=300)
	message = models.TextField()

	def __str__(self):
		return f'{self.user.first_name} {self.user.last_name}: {self.summary}'
