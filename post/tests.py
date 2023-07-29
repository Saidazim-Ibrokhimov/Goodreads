from django.test import TestCase
from django.utils import timezone
from django.urls import reverse 

from .forms import PostUpdateForm, PostCreateForm
from users.models import CustomUser
from django.contrib.auth import get_user
from .models import Post


class PostTestCase(TestCase):
	def setUp(self):
		db_user = CustomUser.objects.create(username='ibrohimov', first_name='aliyev')
		db_user.set_password('parol')
		db_user.save()

		self.client.login(username='ibrohimov', password='parol')

	def test_no_posts(self):
		response = self.client.get(reverse('post:list'))

		self.assertContains(response, 'No posts found.')


	def test_post_list_page(self):
		user1 = CustomUser.objects.create(username='saidazim', email='aks@gmail.com', first_name='Saidazim')
		user1.set_password('password')

		user2 = CustomUser.objects.create(username='saidazimboy', email='boy@ls.uz', first_name='Saidazim2004')
		user2.set_password('somecode')

		post1 = Post.objects.create(title='Post title 1', body='Post body1', muallif=user1)
		post2 = Post.objects.create(title='Post title 2', body='Post body2', muallif=user1)
		post3 = Post.objects.create(title='Post title 3', body='Post body3', muallif=user1)
		post4 = Post.objects.create(title='Post title 4', body='Post body4', muallif=user2)

		response = self.client.get(reverse('post:list'))

		for post in [post1, post2, post3]:
			self.assertContains(response, post.title)
			self.assertContains(response, post.muallif)
			self.assertContains(response, post.body)
			self.assertEqual(post.muallif, user1)
		self.assertContains(response, post4.title)
		self.assertContains(response, post4.body)
		self.assertContains(response, post4.muallif)

		self.assertTemplateUsed(response, 'blog/list.html')





		# user = CustomUser.objects.create(username='saidazim', first_name='Saidazim')
		# user.set_password('somecode')

		# db_user = CustomUser.objects.create(username='saidazifam', first_name='Saidazim')
		# db_user.set_password('password')

		# post1 = Post.objects.create(title='Post title1', slug='Post-title1', body='Some text1', muallif=user, status=Post.Status.published)
		# post2 = Post.objects.create(title='Post title2', slug='Post-title2', body='Some text2', muallif=user, status=Post.Status.published)
		# post3 = Post.objects.create(title='Post title3', slug='Post-title3', body='Some text3', muallif=user, status=Post.Status.published)
		# post4 = Post.objects.create(title='Post title4', slug='Post-title4', body='Some text4', muallif=db_user, status=Post.Status.published)

		# response = self.client.get(reverse('post:list'))

		# for post in [post2, post3]:
		# 	self.assertContains(response, post.title)
		# 	self.assertContains(response, post.muallif)
		# 	self.assertContains(response, post.body)
		# 	self.assertEqual(post.muallif, user)
		# self.assertNotContains(response, post4.title)
		# self.assertNotContains(response, post4.body)
		# self.assertNotContains(response, post4.muallif)

		# self.assertTemplateUsed(response, 'blog/list.html')


	def test_post_detail_page(self):
		user = CustomUser.objects.create(username='saidazim', first_name='Saidazim')
		user.set_password('somecode')
		user.set_password('somecode')

		post = Post.objects.create(title='Post title', slug='Post-title', body='Some text', muallif=user,)

		response = self.client.get(reverse(
			'post:detail', kwargs={'post_slug':post.slug}))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, post.title)		
		self.assertContains(response, post.image)		
		self.assertContains(response, post.body)		
		self.assertContains(response, post.muallif)
		# self.assertContains(response, post.published_date)

		self.assertEqual(post.title, 'Post title')		
		self.assertEqual(post.body, 'Some text')		
		self.assertEqual(post.muallif.first_name, 'Saidazim')		
		self.assertEqual(post.muallif.username, 'saidazim')
		self.assertTemplateUsed(response, 'blog/detail.html')	

	def test_is_post_created(self):
		user = CustomUser.objects.create(
			username='saidazim', 
			first_name='saidazim', 
			last_name='ibrohimov', 
			email='email@gmail.com'
			)
		user.set_password('somecode')
		user.save()

		self.client.login(username='saidazim', password='somecode')

		response = self.client.post(reverse('post:create'),
			data={
			'title':'Atom odatlar',
			'body':'Atom odatlar text',
			})

		client_user = get_user(self.client)

		posts = Post.objects.all()

		form = PostCreateForm()
		self.assertIn('title', form.fields)
		self.assertIn('body', form.fields)
		self.assertIn('image', form.fields)

		self.assertEqual(posts[0].muallif, client_user)
		self.assertEqual(posts.count(), 1)
		self.assertEqual(response.url, reverse('post:list'))
		self.assertEqual(response.status_code, 302)

	def test_post_updated(self):
		user = CustomUser.objects.create(
			username='saidazim', 
			first_name='saidazim', 
			last_name='ibrohimov', 
			email='email@gmail.com'
			)
		user.set_password('somecode')
		user.save()
		self.client.login(username='saidazim', password='somecode')

		post = Post.objects.create(title='Post title', slug='Post-title', body='Some text', muallif=user,)

		response = self.client.post(reverse(
			'post:update', kwargs={'post_slug':post.slug}),
			data={
			'title':'Edited post title',
			'body':'Edited post body'
			}
			)
		post.refresh_from_db()

		form = PostUpdateForm()
		self.assertIn('title', form.fields)
		self.assertIn('body', form.fields)
		self.assertIn('image', form.fields)
		self.assertNotIn('muallif', form.fields)
		self.assertNotIn('published_date', form.fields)

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, reverse(
			'post:detail', 
			kwargs={'post_slug':post.slug}))

		self.assertEqual(post.title, 'Edited post title')
		self.assertEqual(post.body, 'Edited post body')

	def test_post_not_update(self):
		user1 = CustomUser.objects.create(username='Saidazim', email='email@gmail.com', first_name="Saidazim")
		user = CustomUser.objects.create(
			username='saidazim', 
			first_name='saidazim', 
			last_name='ibrohimov', 
			email='email@gmail.com'
			)
		user.set_password('somecode')
		user.save()
		self.client.login(username='saidazim', password='somecode')

		post = Post.objects.create(title='Post title', slug='Post-title', body='Some text', muallif=user1,)
		
		client_user = get_user(self.client)

		response = self.client.post(reverse(
			'post:update', kwargs={'post_slug':post.slug}),
			data={
				'title':'Edited title',
				'body':'Edited body',
			}
		)
		post.refresh_from_db()
		
		self.assertNotEqual(post.title, 'Edited title')
		self.assertNotEqual(post.body, 'Edited body')
		self.assertNotEqual(post.muallif, client_user)

		self.assertEqual(post.title, 'Post title')
		self.assertEqual(post.body, 'Some text')
		self.assertEqual(post.muallif, user1)
		self.assertEqual(response.status_code, 302 )
		self.assertEqual(response.url, reverse('post:list'))

	def test_delete_confirm(self):
		user = CustomUser.objects.create(
			username='saidazim', 
			first_name='saidazim', 
			last_name='ibrohimov', 
			email='email@gmail.com'
			)
		user.set_password('somecode')
		user.save()
		self.client.login(username='saidazim', password='somecode')

		post = Post.objects.create(title='Post title', slug='Post-title', body='Some text', muallif=user,)

		respond = self.client.get(reverse(
			'post:confirm-delete', 
			kwargs={'post_slug':post.slug}
			)
		)
		self.assertContains(respond, post.title)
		self.assertEqual(respond.status_code, 200)

	def test_is_post_deleted(self):
		user1 = CustomUser.objects.create(
			username='saidazimboy', 
			first_name='saidazim', 
			last_name='ibrohimov', 
			email='email@gmail.com')
		
		user = CustomUser.objects.create(
			username='saidazim', 
			first_name='saidazim', 
			last_name='ibrohimov', 
			email='email@gmail.com'
			)
		user.set_password('somecode')
		user.save()
		self.client.login(username='saidazim', password='somecode')

		post1 = Post.objects.create(title='Post title1', slug='Post-title1', body='Some text', muallif=user1,)
		post = Post.objects.create(title='Posttitle2', slug='Posttitle2', body='Some text', muallif=user,)

		response = self.client.get(reverse(
			'post:delete', kwargs={'post_slug':post1.slug}
			)
		)
		
		posts = Post.objects.all()

		self.assertEqual(response.status_code, 302)
		self.assertEqual(posts.count(), 2)
		self.assertEqual(response.url, reverse('post:list'))

		response = self.client.get(reverse('post:delete', kwargs={'post_slug':post.slug}))

		posts= Post.objects.all()

		self.assertEqual(posts.count(), 1)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, reverse('post:list'))

