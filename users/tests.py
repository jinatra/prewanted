import json
import bcrypt

from django.test import TestCase, Client

from users.models import User

class UserTest(TestCase):
    def setUp(self):
        User.objects.bulk_create([
            User(id=1, email='test1@test1.com', password='TESTtest1111!!', nickname='testman1'),
            User(id=2, email='test2@test2.com', password='TESTtest2222!!', nickname='testman2'),
        ])

    def test_signup_post_success(self):
        client = Client()
        data = {
            'email'    : 'test3@test3.com',
            'password' : 'TESTtest3333!!'.encode('utf-8'),
            'nickname' : 'testman3',
        }

        response = client.post('/users/signup', json.dumps(data), content_type = 'application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {
            'STATUS'  : 'SUCCESS',
            'MESSAGE' : 'User Created!'
        })
