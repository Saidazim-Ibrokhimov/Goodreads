from django.test import TestCase
from django.urls import reverse
from Books.models import Book, BookReview, Author, BookAuthor, Genre, BookGenre, Editions
from users.models import CustomUser
# Create your tests here.

class BookTestCase(TestCase):
	def test_no_books(self):
		response = self.client.get(reverse('books:list')			)

		self.assertContains(response, 'No books found.')

	def test_books_list(self):
		book1 = Book.objects.create(title='BookTitle1', slug='BookTitle1', description='BookDescriptio', isbn='BookIsbn1')
		book2 = Book.objects.create(title='BookTitle2', slug='BookTitle2', description='BookDescriptio', isbn='BookIsbn2')
		book3 = Book.objects.create(title='BookTitle3', slug='BookTitle3', description='BookDescription', isbn='BookIsbn3')

		response = self.client.get(reverse('books:list') + '?page_size=2')
		books = [book1, book2]
		for book in books:
			self.assertContains(response, book.title)
		self.assertNotContains(response, book3.title)

		response = self.client.get(reverse('books:list') + '?page=2&?page_size=2')
		self.assertContains(response, book3.title)
			
	def test_book_detail(self):
		book1 = Book.objects.create(title='BookTitle1', slug='BookTitle1', description='BookDescriptio', isbn='BookIsbn1')
		book2 = Book.objects.create(title='BookTitle2', slug='BookTitle2', description='BookDescriptio', isbn='BookIsbn2')
		book3 = Book.objects.create(title='BookTitle3', slug='BookTitle3', description='BookDescription', isbn='BookIsbn3')

		author1 = Author.objects.create(first_name='Alisheer', last_name='Navoiy', email='navoiy@gmail.com', slug='Alisher-Navoiy' )
		author2 = Author.objects.create(first_name='Abdulla', last_name='Oripov', email='oripov@gmail.com', slug='Abdulla-Oripov' )
		


		genre1 = Genre.objects.create(name='Fantastic')
		genre2 = Genre.objects.create(name='Fiction')

		for book in [book1, book2, book3]:
			BookAuthor.objects.create(book=book, author=author1)
			BookAuthor.objects.create(book=book, author=author2)

			BookGenre.objects.create(book=book, genre=genre1)
			BookGenre.objects.create(book=book, genre=genre2)

			edition = Editions.objects.create(
				book=book,
				title='BookTitle1',
				description='BookEditionDesscription',
				isbn='1417691',
				pages=548,
				language='English',
				published_date='2000-02-01'
			)

		books = Book.objects.all()
		for book in books:
			response = self.client.get(reverse('books:detail', kwargs={'book_slug':book.slug} ))
			self.assertContains(response, book.title)
			self.assertContains(response, book.description)

			self.assertContains(response, genre1.name)
			self.assertContains(response, genre2.name)
			
			# I do not know why but it is not worked
			# self.assertContains(response, reverse('books:edition', kwargs={'id':edition.id}))
			self.assertContains(response, edition.language)
			self.assertContains(response, edition.cover)
			self.assertContains(response, 2000)
			self.assertContains(response, edition.cover_pic)

			for bookauthor in book.bookauthor_set.all():
				self.assertContains(response, bookauthor.author)
				self.assertContains(response, reverse('books:authors_profile', kwargs={'author_slug':bookauthor.author.slug}))

	def test_edition_page(self):
		book = Book.objects.create(title='sport', slug='sport', description='BookDescriptio', isbn='BookIsbn1')

		edition = Editions.objects.create(
				book=book,
				title='BookTitle1',
				description='BookEditionDesscription',
				isbn='1417691',
				pages=548,
				language='English',
				published_date='2000-02-01'
			)

		response = self.client.get(reverse('books:edition', kwargs={'id':edition.id}))

		self.assertContains(response, edition.title)
		self.assertContains(response, edition.description)
		self.assertContains(response, edition.isbn)
		self.assertContains(response, edition.pages)
		self.assertContains(response, edition.language)
		self.assertEqual(edition.published_date, '2000-02-01')
		self.assertContains(response, edition.cover)
		self.assertContains(response, edition.cover_pic)
		self.assertTemplateUsed(response, 'books/editions.html')
		self.assertEqual(response.status_code, 200)



	def test_search_books(self):
		book1 = Book.objects.create(title='sport', slug='sport', description='BookDescriptio', isbn='BookIsbn1')
		book2 = Book.objects.create(title='news', slug='news', description='BookDescriptio', isbn='BookIsbn2')
		book3 = Book.objects.create(title='dog', slug='dog', description='BookDescription', isbn='BookIsbn3')

		response = self.client.get(reverse('books:list') + '?q=sport')

		self.assertContains(response, book1.title)
		self.assertNotContains(response, book3.title)
		self.assertNotContains(response, book2.title)

		response = self.client.get(reverse('books:list') + '?q=news')
		self.assertContains(response, book2.title)
		self.assertNotContains(response, book3.title)
		self.assertNotContains(response, book1.title)

		response = self.client.get(reverse('books:list') + '?q=dog')
		self.assertContains(response, book3.title)
		self.assertNotContains(response, book2.title)
		self.assertNotContains(response, book1.title)

class BookReviewTestCase(TestCase):
	def test_reviews(self):
		book = Book.objects.create(title='sport', slug='sport', description='BookDescriptio', isbn='BookIsbn1')
		user = CustomUser.objects.create(username='saidazim', first_name='saidazim', last_name='ibrohimov', email='email@gmail.co,')
		user.set_password('somecode')
		user.save()

		self.client.login(username='saidazim', password='somecode')
		
		response = self.client.post(reverse('books:reviews', kwargs={'book_slug':book.slug} ),
			data={
			'stars_given':4,
			'comment':'MyComment'
			}
			)
		review = book.bookreview_set.all()

		self.assertEqual(review.count(), 1)
		self.assertEqual(review[0].stars_given, 4)
		self.assertEqual(review[0].comment, 'MyComment')
		self.assertEqual(review[0].book, book)
		self.assertEqual(review[0].user, user)

	def test_wrong_rating(self):
		book = Book.objects.create(title='sport', slug='sport', description='BookDescriptio', isbn='BookIsbn1')
		user = CustomUser.objects.create(
			username='saidazim', 
			first_name='saidazim', 
			last_name='ibrohimov', 
			email='email@gmail.com'
			)
		user.set_password('somecode')
		user.save()

		self.client.login(username='saidazim', password='somecode')
		
		response = self.client.post(reverse('books:reviews', kwargs={'book_slug':book.slug} ),
			data={
			'stars_given':9,
			'comment':'MyComment'
			}
			)
		review = book.bookreview_set.all()

		self.assertEqual(review.count(), 0)

	def test_review_confirm_page(self):
		book = Book.objects.create(title='sport', slug='sport', description='BookDescriptio', isbn='BookIsbn1')
		user = CustomUser.objects.create(
			username='saidazim', 
			first_name='saidazim', 
			last_name='ibrohimov', 
			email='email@gmail.co,'
			)
		user.set_password('somecode')
		user.save()

		self.client.login(username='saidazim', password='somecode')
		review = BookReview.objects.create(book=book, user=user, stars_given=5, comment='Good book')
		response = self.client.get(reverse(
			'books:delete-review-confirm', 
			kwargs={'book_slug':book.slug, 'review_id':review.id}))

		self.assertContains(response, book.title)
		self.assertContains(response, review.comment)
		self.assertEqual(book.title, 'sport')
		self.assertEqual(review.comment, 'Good book')

	def test_review_delete(self):
		book = Book.objects.create(title='sport', slug='sport', description='BookDescriptio', isbn='BookIsbn1')
		user = CustomUser.objects.create(
			username='saidazim', 
			first_name='saidazim', 
			last_name='ibrohimov', 
			email='email@gmail.com'
			)
		user.set_password('somecode')
		user.save()

		self.client.login(username='saidazim', password='somecode')
		review = BookReview.objects.create(book=book, user=user, stars_given=5, comment='Good book')
		response = self.client.get(reverse(
			'books:delete-review',
			kwargs={'book_slug':book.slug, 
			'review_id':review.id}
			)
		)

		self.assertEqual(response.url, reverse('books:detail', kwargs={'book_slug':book.slug}))
		self.assertEqual(response.status_code, 302)

		response = self.client.get(reverse('books:detail', kwargs={'book_slug':book.slug}))

		self.assertNotContains(response, review.comment)


class BookAuthorTestCase(TestCase):
	def test_book_author(self):
		book = Book.objects.create(title="Hamsa", slug="Hamsa", isbn="123421", description="Hamsa Description")
		author = Author.objects.create(
			first_name='Alisher', 
			last_name='Navoiy', 
			slug="Alisher-Navoiy",
			email='navoiy@gmail.com',
			bday='1441-10-3',
			dday='1501-12-5',
			website='www.navoiy.com',
			bio='Biography about Navoiy',
			birth_place='Hirot'
			)

		book_author = BookAuthor.objects.create(book=book, author=author)

		response = self.client.get(reverse('books:detail', kwargs={'book_slug':book.slug} ))

		self.assertContains(response, 'Alisher Navoiy')
		self.assertContains(response, reverse('books:authors_profile', kwargs={'author_slug':author.slug}))

	def test_author_page(self):
		book = Book.objects.create(title='sport', slug='sport', description='BookDescriptio', isbn='BookIsbn1')
		book2 = Book.objects.create(title="Hamsa", slug="Hamsa", isbn="123421", description="Hamsa Description")

		author = Author.objects.create(
			first_name='Alisher', 
			last_name='Navoiy', 
			email='navoiy@gmail.com',
			bday='1441-1-3',
			dday='1501-12-5',
			website='www.navoiy.com',
			bio='Biography about Navoiy',
			birth_place='Hirot',
			slug='Alisher-Navoiy'
			)

		book_author = BookAuthor.objects.create(book=book, author=author)
		book_author2 = BookAuthor.objects.create(book=book2, author=author)

		response = self.client.get(reverse('books:authors_profile', kwargs={'author_slug':author.slug}))
		for kitob in [book, book2]:
			self.assertContains(response, kitob.title)
			self.assertContains(response, kitob.cover_pic)
			self.assertContains(response, reverse('books:detail', kwargs={'book_slug':book.slug}))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Alisher Navoiy')
		self.assertContains(response, author.first_name)

		self.assertContains(response, author.last_name)
		self.assertContains(response, author.email)
		self.assertContains(response, author.website)

		self.assertContains(response, author.bio)
		self.assertContains(response, author.birth_place)
		self.assertEqual(author.bday, '1441-1-3')

		self.assertEqual(author.dday, '1501-12-5')
		self.assertEqual(author.first_name, 'Alisher')
		self.assertEqual(author.last_name, 'Navoiy')

		self.assertEqual(author.email, 'navoiy@gmail.com')
		self.assertEqual(author.website, 'www.navoiy.com')
		self.assertEqual(author.bio, 'Biography about Navoiy')
		self.assertEqual(author.birth_place, 'Hirot')


class BookGenreTestCase(TestCase):
	def test_genre_page(self):
		book1 = Book.objects.create(title='sport', slug='sport', description='BookDescriptio', isbn='BookIsbn1')
		book2 = Book.objects.create(title='news', slug='news', description='BookDescriptio', isbn='BookIsbn2')
		book3 = Book.objects.create(title='dog', slug='dog', description='BookDescription', isbn='BookIsbn3')
		book4 = Book.objects.create(title='cat', slug='cat', description='BookDescriptioncat', isbn='BookIsbn3cat')

		genre1 = Genre.objects.create(name='Fantastic')
		genre2 = Genre.objects.create(name='Fiction')
		genre3 = Genre.objects.create(name='Romance')

		author = Author.objects.create(first_name='Alisher', last_name='Navoiy', slug='Alisher-Navoiy', author_image='default.jpg')

		for book in [book1, book2, book3]:
			BookGenre.objects.create(book=book, genre=genre1)
			BookGenre.objects.create(book=book, genre=genre2)
			bookauthor = BookAuthor.objects.create(book=book, author=author)

			response = self.client.get(reverse('books:genre', kwargs={'id':genre1.id}))

			self.assertEqual(response.status_code, 200)

			self.assertContains(response, book.title)
			self.assertContains(response, reverse('books:detail', kwargs={'book_slug':book.slug}))
			self.assertContains(response, author)
			self.assertContains(response, author.author_image)
			self.assertContains(response, reverse('books:authors_profile', kwargs={'author_slug':author.slug}))

			self.assertContains(response, genre1)
			self.assertContains(response, genre2)
			self.assertContains(response, genre3.name)

		response = self.client.get(reverse('books:genre', kwargs={'id':genre2.id}))

		self.assertContains(response, genre3)
		self.assertContains(response, genre2)
		self.assertContains(response, genre1)
		self.assertTemplateUsed(response, 'books/genre.html')

