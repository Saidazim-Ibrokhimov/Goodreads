from django.http import HttpResponse
from django.shortcuts import render 
from Books.models import BookReview
from django.core.paginator import Paginator

def landing_page(request):
	return render(request, "landing.html", {'user':request.user})


def home_page(request):

	book_reviews = BookReview.objects.all().order_by('-created_at')

	page_size = request.GET.get('page_size', 2)
	paginator = Paginator(book_reviews, page_size)
	page_number = request.GET.get('page', 1)

	page_object = paginator.get_page(page_number)

	context = {
		'page_obj':page_object	
	}
	return render(request, 'home.html', context)

