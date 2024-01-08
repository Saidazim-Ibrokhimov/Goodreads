from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.paginator import Paginator 

from hitcount.utils import get_hitcount_model
from django.utils.text import slugify
from hitcount.views import HitCountMixin

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View

from .models import Post
from .forms import PostCreateForm, PostUpdateForm

# Create your views here.

class BlogListView(View):
	def get(self, request):
		posts = Post.objects.all()

		page_size = request.GET.get('page_size', 3)
		paginator = Paginator(posts, page_size)

		page_num = request.GET.get('page', 1)
		page_obj = paginator.get_page(page_num)
	
		return render(request, 'blog/list.html', {'page_obj':page_obj})

class BlogDetailView(View):
	def get(self, request, post_slug):
		posts = Post.objects.all()
		post = Post.objects.get(slug=post_slug)
		context = {
		'post':post,
		'posts':posts
		}

		hit_count = get_hitcount_model().objects.get_for_object(post)
		hits = hit_count.hits
		hitcontext = context['hitcount'] = {'pk':hit_count.pk}
		hit_count_response = HitCountMixin.hit_count(request, hit_count)

		if hit_count_response.hit_counted:
			hits = hits + 1
			hitcontext['hit_counted'] = hit_count_response.hit_counted
			hitcontext['hit_message'] = hit_count_response.hit_message
			hitcontext['total_hits'] = hits

		return render(request, 'blog/detail.html', context)

class BlogCreateView(LoginRequiredMixin, View):
	def get(self, request):
		post_form = PostCreateForm()
		return render(request, 'blog/create.html', {'post_form':post_form})

	def post(self, request):
		post_form = PostCreateForm(data=request.POST, files=request.FILES)
		if post_form.is_valid():
			Post.objects.create(
				muallif=request.user,
				title=post_form.cleaned_data['title'],
				body=post_form.cleaned_data['body'],
				image=post_form.cleaned_data['image'],
				slug=slugify(post_form.cleaned_data['title'])
				)
			messages.success(request, 'Your post will be published within 24 hours!')
			return redirect(reverse('post:list'))
		else:
			return render(request, 'blog/create.html', {'post_form':post_form})

class BlogUpdateView(LoginRequiredMixin, View):
	def get(self, request, post_slug):
		post = Post.objects.get(slug=post_slug)
		update_form = PostUpdateForm(instance=post)
		return render(request, 'blog/update.html', {'update_form':update_form} )

	def post(self, request, post_slug):
		post = Post.objects.get(slug=post_slug)
		update_form = PostUpdateForm(instance=post, data=request.POST, files=request.FILES)
		messages.success(request, 'You have succesfully updated your post!')
		if request.user == post.muallif:
			if update_form.is_valid():
				update_form.save()
				return redirect(reverse('post:detail', kwargs={'post_slug':post.slug}))
			else:
				return render(request, 'blog/update.html', {'update_form':update_form} )
		else:
			messages.warning(request, 'You have no access to edit this post!')
			return redirect(reverse('post:list'))

class BlogDeleteConfirmView(LoginRequiredMixin, View):
	def get(self, request, post_slug):
		post = Post.objects.get(slug=post_slug)
		return render(request, 'blog/confirm_delete.html', {'post':post})

class BlogDeleteView(View):
	def get(self, request, post_slug):	
		post = Post.objects.get(slug=post_slug)
		if request.user == post.muallif:	
			post.delete()
			messages.success(request, 'You have succesfully deleted the post!')
			return redirect(reverse('post:list'))
		else:
			messages.warning(request, 'You can not delete the post!')
			return redirect(reverse('post:list'))

	







