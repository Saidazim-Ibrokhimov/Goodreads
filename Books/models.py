from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import CustomUser

class Book(models.Model):
	title = models.CharField(max_length=500)
	slug = models.SlugField(max_length=500, unique=True)
	description = models.TextField()
	isbn = models.CharField(max_length=17)
	language = models.CharField(max_length=50, default='English')
	published_date = models.DateField(null=True, blank=True)
	pages = models.PositiveIntegerField(default=100)
	cover_pic = models.ImageField(default='default_book_cover.jpg', upload_to='book/')

	def __str__(self):
		return self.title
	
class Shelf(models.Model):
	name = models.CharField(max_length=255)
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	books = models.ManyToManyField(Book, through='BookOnShelf')
	
	def __str__(self):
		return self.name

class BookOnShelf(models.Model):
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE)
	added_on = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f" {self.book.title}  (on {self.shelf.name})"
	

class Editions(models.Model):
	class BookCover(models.TextChoices):
		Paperback = 'Paperback', 'PB'
		Kindle_edition = 'Kindle edition', 'KE'
		Hard_Cover = 'Hard Cover', 'HC'
		Ebook =  'E-book', 'EB'
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	title = models.CharField(max_length=500)
	description = models.TextField()
	isbn = models.CharField(max_length=17)
	pages = models.PositiveIntegerField(default=100)
	cover = models.CharField(max_length=50, choices=BookCover.choices, default=BookCover.Paperback)
	language = models.CharField(max_length=20)
	published_date = models.DateField()
	cover_pic = models.ImageField(default='default_book_cover.jpg', upload_to='book/edition')

	def __str__(self):
		return self.title
		
	class Meta:
		ordering = ['-published_date']
		
class Author(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	slug = models.SlugField(max_length=200, unique=True)
	email = models.EmailField()
	bday = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
	dday = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
	website = models.URLField(max_length=200, null=True, blank=True)
	bio = models.TextField()
	author_image = models.ImageField(upload_to='authors/', default='default_picture.png')
	birth_place = models.CharField(max_length=300, default='Birth place is not provided')

	def __str__(self):
		return f"{self.first_name} {self.last_name}"

	def full_name(self):
		return f"{self.first_name} {self.last_name}"
		

class BookAuthor(models.Model):
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	author = models.ForeignKey(Author, on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.author.first_name}: {self.book}"

	def get_absolute_url(self):
		return reverse('books:authors_profile', args=[self.author.slug])

class Genre(models.Model):
	name = models.CharField(max_length=100, unique=True)

	def __str__(self):
		return self.name

class BookGenre(models.Model):
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.book.title}. Genres: {self.genre.name}"

class BookReview(models.Model):
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	comment= models.TextField()
	stars_given = models.IntegerField(
		validators=[MinValueValidator(1), MaxValueValidator(5)]
		)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.stars_given} stars for {self.book.title} by {self.user.username}"
	
	class Meta:
		ordering = ['-created_at']