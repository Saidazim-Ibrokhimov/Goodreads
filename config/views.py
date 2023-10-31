from django.http import HttpResponse
from django.shortcuts import render
from users.models import CustomUser

def landing_page(request):
	return render(request, "landing.html", {'user':request.user})

def home_page(request):
	return render(request, 'home.html')
