from django.test import TestCase 
from Books.models import Book, BookReview
from django.urls import reverse
from users.models import CustomUser
from django.utils import timezone


class HomePageTestCase(TestCase):
    def test_home_page_paginated_list(self):
        user = CustomUser.objects.create(username='saidazim', first_name='saidazim', last_name='ibrohimov', email='email@gma.co')
        user.set_password('somecode1249&*^*^%$#')
        user.save()

        book = Book.objects.create(title='goodreads', description='About description', isbn='91094011', slug='goodreads')

        now = timezone.now()  # Current time
        days_2 = timezone.now() - timezone.timedelta(days=2)  # Two days ago
        days_3 = timezone.now() - timezone.timedelta(days=3)  # Three days ago
        print('Current date is', now)


        review1 = BookReview.objects.create(user=user, book=book, comment='Awesome book', stars_given=4, created_at=days_3)
        review2 = BookReview.objects.create(user=user, book=book, comment='Great', stars_given=3, created_at=days_2)
        review3 = BookReview.objects.create(user=user, book=book, comment='very good', stars_given=2, created_at=now)

        response = self.client.get(reverse('home_page') + '?page_size=2&page=1')
        print(response)

        self.assertContains(response, review3.comment)
        self.assertContains(response, review3.stars_given)

        self.assertContains(response, review2.comment)
        self.assertContains(response, review2.stars_given)


        self.assertNotContains(response, review1.comment)
        # self.assertNotContains(response, review1.stars_given)

        self.assertContains(response, review3.user.profile_picture.url)
        self.assertContains(response, review3.book.cover_pic.url)







        