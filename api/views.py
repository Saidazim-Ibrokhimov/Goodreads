from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.views import APIView

from Books.models import BookReview
from .serializers import BookReviewSerializer

# Create your views here.

class BookReviewDetailAPIView(APIView):
    def get(self, request, id):
        book_review = BookReview.objects.get(id=id)

        serializer = BookReviewSerializer(book_review)

        return Response(data=serializer.data)
    
class BookReviewListAPIView(APIView):
    def get(self, request):
        book_reviews = BookReview.objects.all()
        serializer = BookReviewSerializer(book_reviews, many=True)
        
        return Response(data=serializer.data)