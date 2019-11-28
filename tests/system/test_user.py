from models.user import UserModel
from tests.base_test import BaseTest
import json

class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/register', data={'username': "test", 'password': "1234"})
                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('test'))
                k = json.loads(response.data)
                self.assertDictEqual({'message': 'User created successfully.'}, k)
    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': "test", 'password': "1234"})
                auth_responce = client.post('/auth',
                                           data=json.dumps({'username': 'test', 'password': "1234"}),
                                           headers={'Content-Type': 'application/json'})
                k = 'access_token'
                l = json.loads(auth_responce.data).keys()
                self.assertIn(k, l)

    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': "test", 'password': "1234"})
                response = client.post('/register', data={'username': "test", 'password': "1234"})
                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': "A user with that username already exists"}, json.loads(response.data))