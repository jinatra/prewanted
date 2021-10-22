import json
import bcrypt
import jwt

from django.test import TestCase, Client

from users.models import User
from my_settings  import SECRET_KEY, ALGORITHM

class SignUpViewTest(TestCase):
    def setUp(self):
        User.objects.bulk_create([
            User(id=1, email='test1@test1.com', password='TESTtest1111!!', nickname='testman1'),
            User(id=2, email='test2@test2.com', password='TESTtest2222!!', nickname='testman2'),
        ])

    def test_signup_post_success(self):
        client = Client()
        data = {
            'email'    : 'test3@test3.com',
            'password' : 'TESTtest3333!!',
            'nickname' : 'testman3',
        }

        response = client.post('/users/signup', json.dumps(data), content_type = 'application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'MESSAGE' : 'user created'})

    def test_singup_post_email_form_error(self):
        client = Client()
        data = {
            'email'    : 'test3test3.com',
            'password' : 'TESTtest3333!!',
            'nickname' : 'testman3',
        }

        response = client.post('/users/signup', json.dumps(data), content_type = 'application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE' : 'wrong e-mail form'})

    def test_singup_post_password_form_error(self):
        client = Client()
        data = {
            'email'    : 'test3@test3.com',
            'password' : 'TESTtest3333',
            'nickname' : 'testman3',
        }

        response = client.post('/users/signup', json.dumps(data), content_type = 'application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE' : 'wrong password form'})

    def test_singup_post_nickname_form_error(self):
        client = Client()
        data = {
            'email'    : 'test3@test3.com',
            'password' : 'TESTtest3333!!',
            'nickname' : '',
        }

        response = client.post('/users/signup', json.dumps(data), content_type = 'application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE' : 'wrong nickname form'})

    def test_signup_post_existing_email_error(self):
        client = Client()
        data = {
            'email'    : 'test1@test1.com',
            'password' : 'TESTtest3333!!',
            'nickname' : 'testman3',
        }

        response = client.post('/users/signup', json.dumps(data), content_type = 'application/json')

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json(), {'MESSAGE' : 'existing e-mail'})

    def test_signup_post_existing_nickname_error(self):
        client = Client()
        data = {
            'email'    : 'test3@test3.com',
            'password' : 'TESTtest3333!!',
            'nickname' : 'testman1',
        }

        response = client.post('/users/signup', json.dumps(data), content_type = 'application/json')

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json(), {'MESSAGE' : 'existing nickname'})

    def test_signup_post_key_error(self):
        client = Client()
        data = {
            'emai'    : 'test3@test3.com',
            'password' : 'TESTtest3333!!',
            'nickname' : 'testman3',
        }

        response = client.post('/users/signup', json.dumps(data), content_type = 'application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE' : 'KEY_ERROR'})

    def tearDown(self):
        User.objects.all().delete()


class SignInViewTest(TestCase):

    def setUp(self):
        password1 = bcrypt.hashpw('TESTtest1111!!'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        password2 = bcrypt.hashpw('TESTtest2222!!'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        User.objects.bulk_create([
            User(id=1, email='test1@test1.com', password=password1, nickname='testman1'),
            User(id=2, email='test2@test2.com', password=password2, nickname='testman2'),
        ])

    def test_signin_post_success(self):
        client = Client()
        data = {
            'email'    : 'test1@test1.com',
            'password' : 'TESTtest1111!!',
        }

        response = client.post('/users/signin', json.dumps(data), content_type = 'application/json')

        token = jwt.encode({'id': 1}, SECRET_KEY, algorithm=ALGORITHM)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
        {
            'MESSAGE'       : 'sign in success',
            'TOKEN'         : token,
            'USER_NICKNAME' : 'testman1'
        })

    def test_signin_post_existing_email_error(self):
        client = Client()
        data = {
            'email'    : 'test3@test3.com',
            'password' : 'TESTtest3333!!',
        }

        response = client.post('/users/signin', json.dumps(data), content_type = 'application/json')

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json(),
        {'MESSAGE' : 'non-existing e-mail'})

    def test_signin_post_wrong_password_error(self):
        client = Client()
        data = {
            'email'    : 'test1@test1.com',
            'password' : 'TESTtest3333!!',
        }

        response = client.post('/users/signin', json.dumps(data), content_type = 'application/json')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),
        {'MESSAGE' : 'wrong password'})

    def test_signin_post_key_error(self):
        client = Client()
        data = {
            'emai'    : 'test1@test1.com',
            'password' : 'TESTtest1111!!',
        }

        response = client.post('/users/signin', json.dumps(data), content_type = 'application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
        {'MESSAGE' : 'KEY_ERROR'})

    def tearDown(self):
        User.objects.all().delete()
