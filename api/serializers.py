from rest_framework import serializers
from Books.models import Book, BookReview
from users.models import CustomUser

class BookSerializer(serializers.ModelSerializer):
        class Meta:
               model = Book
               fields = ('id', 'title', 'description', 'isbn', 'slug', 'language', 'published_date', 'cover_pic', 'pages',)


class CustomUserSerializer(serializers.ModelSerializer):
        class Meta:
                model = CustomUser
                fields = ('id', 'first_name', 'last_name', 'email', 'username')


class BookReviewSerializer(serializers.ModelSerializer):
        book = BookSerializer()
        user = CustomUserSerializer()

        class Meta:
                model = BookReview
                fields = ('id', 'stars_given', 'comment', 'user', 'book',)
