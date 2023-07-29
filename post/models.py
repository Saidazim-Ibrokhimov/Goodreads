from django.db import models
from users.models import CustomUser
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.urls import reverse

from Books.models import Book

# Create your models here.

class Post(models.Model):
	class Status(models.TextChoices):
		draft = 'Draft', 'DR'
		published = 'Published', 'PB'

	title = models.CharField(max_length=500)
	slug = models.SlugField(max_length=500, unique=True)
	image = models.ImageField(upload_to='blog/images', default='25-may.jpg', null=True, blank=True)
	body = RichTextField()
	published_date = models.DateTimeField(default=timezone.now)
	muallif = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.draft)

	class Meta:
		ordering = ['-published_date']

	def __str__(self):
		return self.title

class Category(models.Model):
	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name

class PostCategory(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)

	def __str__(self):
		return f'Category: {self.category.name} | Post: {self.post.title}'
