from django.urls import path
from .views import(
 BookListView, 
 BookDetailView, 
 AddReviewView,
 AuthorProfileView,
 EditReviewView,
 DeleteReviewConfirmView,
 DeleteReviewView,
 BookGenresView,
 BookEditionsView,
 )
 

app_name = 'books'

urlpatterns = [
	path('', BookListView.as_view(), name='list'),
	path('author-profile/<slug:author_slug>/', AuthorProfileView.as_view(), name='authors_profile'),
	path('detail/<slug:book_slug>/', BookDetailView.as_view(), name='detail'),
	path('add-review-for/<slug:book_slug>/', AddReviewView.as_view(), name='reviews'),
	path('edit-review-of/<slug:book_slug>/review/<int:review_id>/', EditReviewView.as_view(), name='edit_review' ),
	path('delete-confirm-review-of/<slug:book_slug>/review/<int:review_id>/', DeleteReviewConfirmView.as_view(), name='delete-review-confirm'),	
	path('delete-review-of/<slug:book_slug>/review/<int:review_id>/', DeleteReviewView.as_view(), name='delete-review'),
	path('genres/<int:id>/', BookGenresView.as_view(), name='genre'),
	path('editions/<int:id>/', BookEditionsView.as_view(), name='edition'),
]	