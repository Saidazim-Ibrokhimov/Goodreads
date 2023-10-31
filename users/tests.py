from django.contrib.auth import get_user
from django.test import TestCase
from django.urls import reverse

from .forms import MessageForm
from users.models import CustomUser, Contact


# Create your tests here.

class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse("users:register"),
                         data={
                'username':'saidazim123',
                'first_name':'saidazim',
                'last_name':'ibrohimov',
                'email':'saidazim@gmail.com',
                'password':'ISBQ1248'

            }
        )

        user = CustomUser.objects.get(username="saidazim123")

        self.assertEqual(user.first_name, 'saidazim')
        self.assertEqual(user.last_name, 'ibrohimov')
        self.assertEqual(user.email, 'saidazim@gmail.com')
        self.assertNotEqual(user.password, 'ISBQ1248')
        self.assertTrue(user.check_password('ISBQ1248'))


    def test_required_fields(self):
            response = self.client.post(
                reverse("users:register"),
                    data={
                    'first_name':'saidazim',
                    'last_name':'ibrohimov',
                    'email':'email@gmail.com'
                    }
                )

            user_count = CustomUser.objects.count()

            self.assertEqual(user_count, 0)
            self.assertFormError(response, 'form', 'username', 'This field is required.')
            self.assertFormError(response, 'form', 'password', 'This field is required.')

    def test_valid_email(self):
        response = self.client.post(
            reverse("users:register"),
            data={
            'username':'alihoja',
            'first_name':'ali',
            'last_name':'valiyev',
            'email':'just_email',
            'password':'parol'
            }
            )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')



    def test_unique_username(self):
        response1 = self.client.post(
            reverse("users:register"),
                data={
                'username':'saidazimboy',
                'first_name':'saidazim',
                'last_name':'ibrohimov',
                'email':'email@gmail.com',
                'password':'somecode'
                }
            )

        response2 = self.client.post(
            reverse('users:register'),
                data={
                'username':'saidazimboy',
                'first_name':'xurshid',
                'last_name':'ortiqboyev',
                'password':'134qwerty',
                'email':'email@gmail.com',

                }
            )

        user_count = CustomUser.objects.count()
        user1 = CustomUser.objects.get(username='saidazimboy')

        self.assertEqual(user_count, 1)
        self.assertFormError(response2, 'form', 'username', 'A user with that username already exists.')
        self.assertTrue(user1.check_password('somecode'))

class LoginTestCase(TestCase):
    def setUp(self):
        db_user = CustomUser.objects.create(username='ibrohimov', first_name='aliyev')
        db_user.set_password('parol')
        db_user.save()

    def test_user_succesful_login(self):
         self.client.post(
            reverse('users:login'),
                data={
            'username':'ibrohimov',
            'password':'parol'
            }
            )
         user = get_user(self.client)

         self.assertTrue(user.is_authenticated)

    def test_wrong_crediantials(self):
         self.client.post(
            reverse('users:login'),
                data={
            'username':'ibrohimovs',
            'password':'parol'
            }
            )
         user = get_user(self.client)

         self.assertFalse(user.is_authenticated)

         self.client.post(
			 reverse('users:login'), data={'username':'ibrohimov','password':'parolm'})

         user = get_user(self.client)
         self.assertFalse(user.is_authenticated)

    def test_logout(self):
        self.client.login(username='ibrohimov', password='parol')
        self.client.get(reverse('users:logout'))

        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)



class ProfilePageTescase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse('users:profile_page'))

        self.assertEqual(response.url, reverse('users:login')  + '?next=/users/profile/')
        self.assertEqual(response.status_code, 302)

    def test_profile_detail(self):
        user = CustomUser.objects.create(username='saidazim', first_name='saidazim', last_name='ibrohimov', email='email@gmail.co,')
        user.set_password('somecode')
        user.save()

        self.client.login(username='saidazim', password='somecode')

        response = self.client.get(reverse('users:profile_page'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_update_profile(self):
        user = CustomUser.objects.create(username='saidazim', first_name='saidazim', last_name='ibrohimov', email='email@gmail.co,')
        user.set_password('somecode')
        user.save()

        self.client.login(username='saidazim', password='somecode')

        response = self.client.post(
            reverse('users:profile_edit'),
            data={'username':'saidazim', 'first_name':'Saidazim', 'last_name':'Ibrohimov', 'email':'Email@gmail.com'}
            )
        user.refresh_from_db()

        self.assertEqual(user.first_name, 'Saidazim')
        self.assertEqual(user.last_name, 'Ibrohimov')
        self.assertEqual(response.url, reverse('users:profile_page'))

class ContactTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse('users:contact'))

        self.assertEqual(response.url, reverse('users:login')  + '?next=/users/contact/')
        self.assertEqual(response.status_code, 302)

    def test_contact_page(self):
        user = CustomUser.objects.create(username='saidazim', first_name='saidazim', last_name='ibrohimov', email='email@gmail.co,')
        user.set_password('somecode')
        user.save()

        self.client.login(username='saidazim', password='somecode')

        form = MessageForm()

        response = self.client.get(reverse('users:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
        self.assertIn('summary', form.fields)
        self.assertIn('message', form.fields)



        response = self.client.post(reverse('users:contact'),
            data = {
            'user':user,
            'summary':'Contact summary',
            'message':'Contact message'
            }
            )
        message = Contact.objects.get(id=1)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(message.summary, 'Contact summary')
        self.assertEqual(message.message, 'Contact message')
