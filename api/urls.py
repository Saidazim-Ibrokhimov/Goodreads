from django.urls import path
from .views import BookReviewDetailAPIView, BookReviewListAPIView

app_name = 'api'
urlpatterns = [
    path('review/<int:id>/', BookReviewDetailAPIView.as_view(), name='review_detail'),
    path('reviews/', BookReviewListAPIView.as_view(), name='reviews_list'),
]
