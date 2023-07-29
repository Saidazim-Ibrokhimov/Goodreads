from django.urls import path
from .views import *

app_name = 'post'

urlpatterns = [
	path('', BlogListView.as_view(), name='list'),
	path('detail/<slug:post_slug>/', BlogDetailView.as_view(), name='detail'),
	path('new/post/', BlogCreateView.as_view(), name='create'),
	path('edit/<slug:post_slug>/', BlogUpdateView.as_view(), name='update'),
	path('confirm-delete/<slug:post_slug>/', BlogDeleteConfirmView.as_view(), name='confirm-delete'),
	path('delete/<slug:post_slug>/', BlogDeleteView.as_view(), name='delete')
]