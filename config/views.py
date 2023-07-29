from django.http import HttpResponse
from django.shortcuts import render 

def landing_page(request):
	print(request.headers['User-Agent'])
	return render(request, "landing.html", {'user':request.user})


def home_page(request):
	return render(request, 'home.html')

