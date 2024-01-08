from pprint import pprint
from Books.models import Book, BookReview
from users.models import CustomUser

from rest_framework.test import APITestCase
from rest_framework.reverse import reverse


# Create your tests here.

class BookReviewAPITestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(username='saidazim', first_name='saidazim', last_name='ibrohimov', email='email@gma.co')
        self.user.set_password('somepass')
        self.user.save()

    def test_book_review_detail(self):
        book = Book.objects.create(title='goodreads', description='About description', isbn='91094011', slug='goodreads')
        review = BookReview.objects.create(user=self.user, book=book, comment='Awesome book', stars_given=4)

        response = self.client.get(reverse('api:review_detail', kwargs={'id':review.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], review.id)
        self.assertEqual(response.data['comment'], review.comment)
        self.assertEqual(response.data['stars_given'], review.stars_given)

        self.assertEqual(response.data['book']['id'], book.id)
        self.assertEqual(response.data['book']['title'], book.title)
        self.assertEqual(response.data['book']['description'], book.description)
        self.assertEqual(response.data['book']['isbn'], book.isbn)
        self.assertEqual(response.data['book']['slug'], book.slug)

        self.assertEqual(response.data['user']['id'], self.user.id)
        self.assertEqual(response.data['user']['username'], self.user.username)
        self.assertEqual(response.data['user']['first_name'], self.user.first_name)
        self.assertEqual(response.data['user']['last_name'], self.user.last_name)
        self.assertEqual(response.data['user']['email'], self.user.email)

    def test_delete_review(self):
        book = Book.objects.create(title='goodreads', description='About description', isbn='91094011', slug='goodreads')
        review = BookReview.objects.create(user=self.user, book=book, comment='Awesome book', stars_given=5)

        response = self.client.delete(reverse('api:review_detail', kwargs={'id':review.id}))

        self.assertEqual(response.status_code, 204)
        self.assertFalse(BookReview.objects.filter(id=review.id).exists())

    def test_patch_review(self):
        book = Book.objects.create(title='goodreads', description='About description', isbn='91094011', slug='goodreads')
        review = BookReview.objects.create(user=self.user, book=book, comment='Awesome book', stars_given=4)

        response = self.client.patch(reverse('api:review_detail', kwargs={'id':review.id}), data={'stars_given':4})
        review.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(review.stars_given, 4)

    def test_put_review(self):
        book = Book.objects.create(title='goodreads', description='About description', isbn='91094011', slug='goodreads')
        review = BookReview.objects.create(user=self.user, book=book, comment='Awesome book', stars_given=4)

        response = self.client.put(
            reverse('api:review_detail', kwargs={'id':review.id}),
             data={
                'comment':'Very good ...',
                'stars_given':2,
                'user_id':self.user.id,
                'book_id':book.id
            }
        )

        review.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(review.stars_given, 2)
        self.assertEqual(review.comment, 'Very good ...')

    def test_post_review(self):
        book = Book.objects.create(title='goodreads', description='About description', isbn='91094011', slug='goodreads')

        data={
            'stars_given':4,
            'comment':'Awesome book about django',
            'user_id':self.user.id,
            'book_id':book.id
        }

        response = self.client.post(reverse('api:reviews_list'), data=data)
        review = BookReview.objects.get(book=book)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(review.stars_given, 4)
        self.assertEqual(review.comment, "Awesome book about django")



    
    def test_book_review_list(self):
        user2 = CustomUser.objects.create(username='Ibrohimov', first_name='saidazim', last_name='ibrohimov', email='email@gma.co')
        user2.set_password('somepass')
        user2.save()

        book = Book.objects.create(title='goodreads', description='About description', isbn='91094011', slug='goodreads')

        review1 = BookReview.objects.create(user=self.user, book=book, comment='Awesome book', stars_given=4)
        review2 = BookReview.objects.create(user=user2, book=book, comment='Great', stars_given=5)

        response = self.client.get(reverse('api:reviews_list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)

        self.assertEqual(response.data['results'][0]['id'], review2.id)
        self.assertEqual(response.data['results'][0]['comment'], review2.comment)
        self.assertEqual(response.data['results'][0]['stars_given'], review2.stars_given)

        self.assertEqual(response.data['results'][1]['id'], review1.id)
        self.assertEqual(response.data['results'][1]['stars_given'], review1.stars_given)
        self.assertEqual(response.data['results'][1]['comment'], review1.comment)


        


        
