import json
import jwt

from django.test import TestCase, Client

from boards.models import Board
from users.models  import User
from my_settings   import SECRET_KEY, ALGORITHM

class BoardCreateViewTest(TestCase):

    def setUp(self):
        user1 = User.objects.create(id=1, email='test1@test1.com', password='TESTtest1111!!', nickname='testman1')
        user2 = User.objects.create(id=2, email='test2@test2.com', password='TESTtest2222!!', nickname='testman2')
        user3 = User.objects.create(id=3, email='test3@test3.com', password='TESTtest3333!!', nickname='testman3')

        board1 = Board.objects.create(id=1, title='test title 1', content='test content 1', user=user1)
        board1 = Board.objects.create(id=2, title='test title 2', content='test content 2', user=user2)


    def test_board_create_post_success(self):
        client = Client()

        token = jwt.encode({'id' : 3}, SECRET_KEY, algorithm=ALGORITHM)
        headers      = {"HTTP_Authorization": token}   

        data = {
            'title'   : 'test title 3',
            'content' : 'test content 3',
        }

        response = client.post('/boards/create', json.dumps(data), content_type = 'application/json', **headers)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'MESSAGE' : {
            'title'         : 'test title 3',
            'content'       : 'test content 3',
            'user_id'       : 3,
            'user_nickname' : 'testman3'
        }})

