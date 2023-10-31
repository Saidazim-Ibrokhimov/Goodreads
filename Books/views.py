from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator 
from django.views import View

from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Book, BookReview, Author, Genre, Editions, Shelf
from .forms import BookReviewForm

# Create your views here.

class BookListView(View):
	def get(self, request):
		books = Book.objects.all().order_by('id')
		search_query = request.GET.get('q', '')

		if search_query:
 			books = books.filter(title__icontains=search_query)
			 
		page_size = request.GET.get('page_size', 2)
		paginator = Paginator(books, page_size)

		page_num = request.GET.get('page', 1)
		page_obj = paginator.get_page(page_num)

		return render(request, 'books/list.html', {'page_obj':page_obj, 'search_query':search_query})

class BookDetailView(View):
	def get(self, request, book_slug):
		book = Book.objects.get(slug=book_slug)

		bookauthors = book.bookauthor_set.all()
		book_genre = book.bookgenre_set.all()
		editions = Editions.objects.filter(book=book)

		review_form = BookReviewForm()
		context = {
				'book':book,
				'review_form':review_form,
				'bookauthors':bookauthors,
				'book_genre':book_genre,
				'editions':editions,
			}
		
		if request.user.is_authenticated:
			shelves = Shelf.objects.filter(user=request.user)
			context['shelves'] = shelves
 
		return render(request, 'books/detail.html', context )


class BookGenresView(View):
	def get(self, request, id):
		genres = Genre.objects.all()
		genre = Genre.objects.get(id=id)
		
		context = {
			'genres':genres,
			'genre':genre
		}
		return render(request, 'books/genre.html', context)

class BookEditionsView(View):
	def get(self, request, id):
		edition = Editions.objects.get(id=id)

		context = {
		'edition':edition,
		}

		return render(request, 'books/editions.html', context)

class AddReviewView(LoginRequiredMixin, View):
	def post(self, request, book_slug):
		book = Book.objects.get(slug=book_slug)
		review_form = BookReviewForm(data=request.POST)

		if review_form.is_valid():
			BookReview.objects.create(
				book = book,
				user = request.user,
				stars_given = review_form.cleaned_data['stars_given'],
				comment = review_form.cleaned_data['comment']
				)
			return redirect(reverse('books:detail', kwargs={'book_slug':book.slug}))
		return render(request, 'books/detail.html', {'book':book, 'review_form':review_form })

class EditReviewView(LoginRequiredMixin, View):
	def get(self, request, book_slug, review_id):
		book = Book.objects.get(slug=book_slug)
		review = book.bookreview_set.get(id=review_id)
		review_form = BookReviewForm(instance=review)
		return render(request, 'books/edit_review.html', {'book':book, 'review':review, 'review_form':review_form})

	def post(self, request, book_slug, review_id):
		book = Book.objects.get(slug=book_slug)
		review = book.bookreview_set.get(id=review_id)
		review_form = BookReviewForm(instance=review, data=request.POST)

		if review_form.is_valid():
			review_form.save()
			return redirect(reverse('books:detail', kwargs={'book_slug':book.slug}))

class DeleteReviewConfirmView(LoginRequiredMixin, View):
	def get(self, request, book_slug, review_id):
		book = Book.objects.get(slug=book_slug)
		review = book.bookreview_set.get(id=review_id)
		return render(request, 'books/delete_review_confirm.html', {'book':book, 'review':review})

class DeleteReviewView(LoginRequiredMixin, View):
	def get(self, request, book_slug, review_id):
		book = Book.objects.get(slug=book_slug)
		review = book.bookreview_set.get(id=review_id)
		if request.user == review.user:
			review.delete()
			messages.success(request, 'You have succesfully deleted this review!')
			return redirect(reverse('books:detail', kwargs={'book_slug':book.slug}))
		else:
			messages.warning(request, 'You have no access to detelte the review')
			return redirect(reverse('books:detail', kwargs={'book_slug':book.slug}))


class AuthorProfileView(View):
	def get(self, request, author_slug):
		author = Author.objects.get(slug=author_slug)
		books = author.bookauthor_set.all()
		return render(request, 'authors/author_page.html', {'author':author, 'books':books})


@login_required
def create_shelf(request):
	if request.method == 'POST':
		name = request.POST['name']
		shelf = Shelf.objects.create(name=name, user=request.user)
		return redirect('home_page')
	return render(request, 'books/detail.html')

@login_required
def add_book_to_shelf(request, book_id, shelf_id):
	book = get_object_or_404(Book, id=book_id)
	shelf = get_object_or_404(Shelf, id=shelf_id)

	shelf.book.add(book)
	shelf.save()

	return redirect(reverse('books:detail', kwargs={'book_slug':book.slug}))
