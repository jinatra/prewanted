import json
import jwt
import mock
import datetime

from django.http import response
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
        board2 = Board.objects.create(id=2, title='test title 2', content='test content 2', user=user2)


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

    def test_board_title_length_error(self):
        client = Client()

        token = jwt.encode({'id' : 3}, SECRET_KEY, algorithm=ALGORITHM)
        headers      = {"HTTP_Authorization": token}   

        data = {
            'title'   : '',
            'content' : 'test content 3',
        }

        response = client.post('/boards/create', json.dumps(data), content_type = 'application/json', **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE' : 'please fill in both title and content'})

    def test_board_content_length_error(self):
        client = Client()

        token = jwt.encode({'id' : 3}, SECRET_KEY, algorithm=ALGORITHM)
        headers      = {"HTTP_Authorization": token}   

        data = {
            'title'   : 'test title 3',
            'content' : '',
        }

        response = client.post('/boards/create', json.dumps(data), content_type = 'application/json', **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE' : 'please fill in both title and content'})

    def test_board_key_error(self):
        client = Client()

        token = jwt.encode({'id' : 3}, SECRET_KEY, algorithm=ALGORITHM)
        headers      = {"HTTP_Authorization": token}   

        data = {
            'titl'   : 'test title 3',
            'content' : 'test content 3',
        }

        response = client.post('/boards/create', json.dumps(data), content_type = 'application/json', **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE' : 'KEY_ERROR'})

    def tearDown(self):
        Board.objects.all().delete()
        User.objects.all().delete()


class BoardListViewTest(TestCase):
    def setUp(self):
        user1 = User.objects.create(id=1, email='test1@test1.com', password='TESTtest1111!!', nickname='testman1')
        user2 = User.objects.create(id=2, email='test2@test2.com', password='TESTtest2222!!', nickname='testman2')
        user3 = User.objects.create(id=3, email='test3@test3.com', password='TESTtest3333!!', nickname='testman3')

        board1 = Board.objects.create(id=1, title='test title 1', content='test content 1', user=user1)
        board2 = Board.objects.create(id=2, title='test title 2', content='test content 2', user=user2)
        board3 = Board.objects.create(id=3, title='test title 3', content='test content 3', user=user1)
        board4 = Board.objects.create(id=4, title='test title 4', content='test content 4', user=user2)
        board5 = Board.objects.create(id=5, title='test title 5', content='test content 5', user=user1)

    def test_board_list_get_success(self):
        client = Client()

        response = client.get('/boards/list?OFFSET=0&LIMIT=1')
        testtime = datetime.datetime.now()

        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = testtime

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'MESSAGE' : {
            'count' : 1,
            'data' : [
                {
                    'title'         : 'test title 1',
                    'content'       : 'test content 1',
                    'user_id'       : 1,
                    'user_nickname' : 'testman1',
                    'created_at'    : testtime.strftime('%Y-%m-%d %H:%M:%S')
                }
            ]
        }})

    def tearDown(self):
        Board.objects.all().delete()
        User.objects.all().delete()


class BoardListViewTest(TestCase):
    def setUp(self):
        user1 = User.objects.create(id=1, email='test1@test1.com', password='TESTtest1111!!', nickname='testman1')
        board1 = Board.objects.create(id=1, title='test title 1', content='test content 1', user=user1)

    def test_board_read_get_success(self):
        client = Client()

        response = client.get('/boards/read/1')
        testtime = datetime.datetime.now()

        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = testtime

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'MESSAGE' : {
            'title'         : 'test title 1',
            'content'       : 'test content 1',
            'user_id'       : 1,
            'user_nickname' : 'testman1',
            'created_at'    : testtime.strftime('%Y-%m-%d %H:%M:%S')
        }})

    def test_board_read_not_existing_error(self):
        client = Client()

        response = client.get('/boards/read/45')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'MESSAGE' : 'non-existing board'})

    def test_board_read_key_error(self):
        client = Client()

        response = client.get('/boards/read/')

        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        Board.objects.all().delete()
        User.objects.all().delete()

class BoardUpdateViewTest(TestCase):
    def setUp(self):
        user1 = User.objects.create(id=1, email='test1@test1.com', password='TESTtest1111!!', nickname='testman1')
        board1 = Board.objects.create(id=1, title='test title 1', content='test content 1', user=user1)

    def test_board_update_post_success(self):
        client = Client()

        token   = jwt.encode({'id' : 1}, SECRET_KEY, algorithm=ALGORITHM)
        headers = {"HTTP_Authorization": token}   

        data = {
            'new_title'   : 'new test title',
            'new_content' : 'new test content',
        }

        response = client.post('/boards/update/1', json.dumps(data), content_type = 'application/json', **headers)
        testtime = datetime.datetime.now()

        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = testtime

        self.assertEqual(response.json(), {'MESSAGE' : 'board edited', 'UPDATE_TIME' : testtime.strftime('%Y-%m-%d %H:%M:%S')})
        self.assertEqual(response.status_code, 200)

    def test_board_update_post_none_existing_board_error(self):
        client = Client()

        token   = jwt.encode({'id' : 1}, SECRET_KEY, algorithm=ALGORITHM)
        headers = {"HTTP_Authorization": token}   

        data = {
            'new_title'   : 'new test title',
            'new_content' : 'new test content',
        }

        response = client.post('/boards/update/50', json.dumps(data), content_type = 'application/json', **headers)
        testtime = datetime.datetime.now()

        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = testtime

        self.assertEqual(response.json(), {'MESSAGE' : 'non-existing board'})
        self.assertEqual(response.status_code, 404)

    def test_board_update_post_editing_board_title_length_none_error(self):
        client = Client()

        token   = jwt.encode({'id' : 1}, SECRET_KEY, algorithm=ALGORITHM)
        headers = {"HTTP_Authorization": token}   

        data = {
            'new_title'   : '',
            'new_content' : 'new test content',
        }

        response = client.post('/boards/update/1', json.dumps(data), content_type = 'application/json', **headers)
        testtime = datetime.datetime.now()

        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = testtime

        self.assertEqual(response.json(), {'MESSAGE' : 'please fill in both title and content'})
        self.assertEqual(response.status_code, 400)

    def test_board_update_post_editing_board_content_length_none_error(self):
        client = Client()

        token   = jwt.encode({'id' : 1}, SECRET_KEY, algorithm=ALGORITHM)
        headers = {"HTTP_Authorization": token}   

        data = {
            'new_title'   : 'new test title',
            'new_content' : '',
        }

        response = client.post('/boards/update/1', json.dumps(data), content_type = 'application/json', **headers)
        testtime = datetime.datetime.now()

        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = testtime

        self.assertEqual(response.json(), {'MESSAGE' : 'please fill in both title and content'})
        self.assertEqual(response.status_code, 400)

    def test_board_update_post_key_error(self):
        client = Client()

        token   = jwt.encode({'id' : 1}, SECRET_KEY, algorithm=ALGORITHM)
        headers = {"HTTP_Authorization": token}   

        data = {
            'new_titl'   : 'new test title',
            'new_content' : 'new test content',
        }

        response = client.post('/boards/update/1', json.dumps(data), content_type = 'application/json', **headers)
        testtime = datetime.datetime.now()

        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = testtime

        self.assertEqual(response.json(), {'MESSAGE' : 'KEY_ERROR'})
        self.assertEqual(response.status_code, 400)

    def tearDown(self):
        Board.objects.all().delete()
        User.objects.all().delete()


class BoardDeleteViewTest(TestCase):
    def setUp(self):
        user1 = User.objects.create(id=1, email='test1@test1.com', password='TESTtest1111!!', nickname='testman1')
        user2 = User.objects.create(id=2, email='test2@test2.com', password='TESTtest2222!!', nickname='testman2')

        board1 = Board.objects.create(id=1, title='test title 1', content='test content 1', user=user1)


    def test_board_delete_success(self):
        client  = Client()

        token   = jwt.encode({'id' : 1}, SECRET_KEY, algorithm=ALGORITHM)
        headers = {"HTTP_Authorization": token}  
        
        response = client.delete('/boards/delete/1', **headers)

        self.assertEqual(response.json(), {'MESSAGE' : 'board deleted'})
        self.assertEqual(response.status_code, 200)

    def test_board_delete_board_not_exists_error(self):
        client  = Client()

        token   = jwt.encode({'id' : 1}, SECRET_KEY, algorithm=ALGORITHM)
        headers = {"HTTP_Authorization": token}  
        
        response = client.delete('/boards/delete/2', **headers)

        self.assertEqual(response.json(), {'MESSAGE' : 'board-not-exists'})
        self.assertEqual(response.status_code, 404)

    def test_board_delete_wrong_user_error(self):
        client  = Client()

        token   = jwt.encode({'id' : 2}, SECRET_KEY, algorithm=ALGORITHM)
        headers = {"HTTP_Authorization": token}  
        
        response = client.delete('/boards/delete/1', **headers)

        self.assertEqual(response.json(), {'MESSAGE' : 'wrong user'})
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        Board.objects.all().delete()
        User.objects.all().delete()