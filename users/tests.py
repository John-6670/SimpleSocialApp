from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import Profile


# Create your tests here.
class TestSetup(TestCase):
    def setUp(self):
        self.client = APIClient()


class TestCreateUser(TestSetup):
    def test_create_user(self):
        response = self.client.post('/users/register/', {'username': 'testUser', 'password': 'testPass',
                                                         'confirm_password': 'testPass', 'email': 'test@test.com',
                                                         'first_name': 'test', 'last_name': 'user'})
        self.assertEqual(response.status_code, 201, 'Status code is not 201')

    def test_create_user_no_password(self):
        response = self.client.post('/users/register/', {'username': 'testUser'})
        self.assertEqual(response.status_code, 400, 'Status code is not 400')

    def test_create_user_no_username(self):
        response = self.client.post('/users/register/', {'password': 'testPass'})
        self.assertEqual(response.status_code, 400, 'Status code is not 400')

    def test_create_user_no_confirm_password(self):
        response = self.client.post('/users/register/', {'username': 'testUser', 'password': 'testPass'})
        self.assertEqual(response.status_code, 400, 'Status code is not 400')

    def test_create_user_passwords_dont_match(self):
        response = self.client.post('/users/register/', {'username': 'testUser', 'password': 'testPass',
                                                         'confirm_password': 'notTestPass'})
        self.assertEqual(response.status_code, 400, 'Status code is not 400')

    def test_create_user_no_email(self):
        response = self.client.post('/users/register/', {'username': 'testUser', 'password': 'pass',
                                                         'confirm_password': 'pass',
                                                         'first_name': 'test', 'last_name': 'user'})
        self.assertEqual(response.status_code, 201, 'Status code is not 201')

    def test_create_user_no_first_name(self):
        response = self.client.post('/users/register/', {'username': 'testUser', 'password': 'pass',
                                                         'confirm_password': 'pass', 'email': 'test@test.com',
                                                         'last_name': 'user'})
        self.assertEqual(response.status_code, 201, 'Status code is not 201')

    def test_create_user_no_last_name(self):
        response = self.client.post('/users/register/', {'username': 'testUser', 'password': 'pass',
                                                         'confirm_password': 'pass', 'email': 'test@test.com',
                                                         'first_name': 'test'})
        self.assertEqual(response.status_code, 201, 'Status code is not 201')


class TestLoginUser(TestSetup):
    def setUp(self):
        super().setUp()
        self.client.post('/users/register/', {'username': 'testUser', 'password': 'testPass',
                                              'confirm_password': 'testPass'})

    def test_login_user(self):
        self.client.post('/users/register/', {'username': 'testUser', 'password': 'testPass',
                                              'confirm_password': 'testPass'})
        response = self.client.post('/users/login/', {'username': 'testUser', 'password': 'testPass'})
        self.assertEqual(response.status_code, 200, 'Status code is not 200')

    def test_login_user_no_username(self):
        response = self.client.post('/users/login/', {'password': 'testPass'})
        self.assertEqual(response.status_code, 400, 'Status code is not 400')

    def test_login_user_no_password(self):
        response = self.client.post('/users/login/', {'username': 'testUser'})
        self.assertEqual(response.status_code, 400, 'Status code is not 400')

    def test_login_user_wrong_password(self):
        response = self.client.post('/users/login/', {'username': 'testUser', 'password': 'wrongPass'})
        self.assertEqual(response.status_code, 401, 'Status code is not 400')

    def test_login_user_wrong_username(self):
        response = self.client.post('/users/login/', {'username': 'wrongUser', 'password': 'testPass'})
        self.assertEqual(response.status_code, 401, 'Status code is not 400')


class TestLogoutUser(TestSetup):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create(username='testUser', password='testPass')
        self.refresh = str(RefreshToken.for_user(self.user))

    def test_logout_user(self):
        response = self.client.post('/users/logout/', {'refresh': self.refresh})
        self.assertEqual(response.status_code, 200, 'Status code is not 204')

    def test_logout_user_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.post('/users/logout/', {'refresh': 'wrongRefreshToken'})
        self.assertEqual(response.status_code, 400, 'Status code is not 401')


class TestFollowUser(TestSetup):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create(username='testUser', password='testPass')
        self.user2 = User.objects.create(username='testUser2', password='testPass')
        self.client.force_authenticate(user=self.user)

    def test_follow_user(self):
        response = self.client.post(f'/users/{self.user2.username}/follow/')
        self.assertEqual(response.status_code, 201, 'Status code is not 201')

    def test_follow_user_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(f'/users/{self.user2.username}/follow/')
        self.assertEqual(response.status_code, 401, 'Status code is not 401')

    def test_unfollow_user(self):
        self.client.post(f'/users/{self.user2.username}/follow/')
        response = self.client.post(f'/users/{self.user2.username}/follow/')
        self.assertEqual(response.status_code, 204, 'Status code is not 204')

    def test_unfollow_user_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(f'/users/{self.user2.username}/follow/')
        self.assertEqual(response.status_code, 401, 'Status code is not 401')

    def test_follow_user_does_not_exist(self):
        response = self.client.post('/users/notAUser/follow/')
        self.assertEqual(response.status_code, 404, 'Status code is not 404')


class TestShowUser(TestSetup):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create(username='testUser', password='testPass')
        self.client.force_authenticate(user=self.user)

    def test_show_profile(self):
        response = self.client.get('/users/profile/')
        self.assertEqual(response.status_code, 200, 'Status code is not 200')

    def test_show_profile_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get('/users/profile/')
        self.assertEqual(response.status_code, 401, 'Status code is not 401')

    def test_show_user_does_not_exist(self):
        response = self.client.get('/users/notAUser/')
        self.assertEqual(response.status_code, 404, 'Status code is not 404')

    def test_show_user(self):
        new_user = User.objects.create(username='newUser', password='newPass')
        response = self.client.get(f'/users/{new_user.username}/')
        self.assertEqual(response.status_code, 200, 'Status code is not 200')

    def test_show_user_unauthenticated(self):
        self.client.force_authenticate(user=None)
        new_user = User.objects.create(username='newUser', password='newPass')
        response = self.client.get(f'/users/{new_user.username}/')
        self.assertEqual(response.status_code, 200, 'Status code is not 200')


class ProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testUser', password='testPass')

    def test_profile_created(self):
        self.assertIsNotNone(Profile.objects.get(user=self.user))

    def test_profile_retrieved(self):
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.user.username, 'testUser')

    def test_profile_updated(self):
        profile = Profile.objects.get(user=self.user)
        profile.bio = 'Test bio'
        profile.save()
        updated_profile = Profile.objects.get(user=self.user)
        self.assertEqual(updated_profile.bio, 'Test bio')

    def test_profile_deleted(self):
        profile = Profile.objects.get(user=self.user)
        profile.delete()
        with self.assertRaises(Profile.DoesNotExist):
            Profile.objects.get(user=self.user)


class TestRefreshEndpoint(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testUser', password='testPass')
        self.refresh = str(RefreshToken.for_user(self.user))

    def test_endpoint(self):
        response = self.client.post('/users/refresh/', {'refresh': self.refresh})
        self.assertEqual(response.status_code, 200)


class TestVerifyEndpoint(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testUser', password='testPass')
        self.token = str(RefreshToken.for_user(self.user).access_token)

    def test_endpoint(self):
        response = self.client.post('/users/verify/', {'token': self.token})
        self.assertEqual(response.status_code, 200)


class TestBlacklistEndpoint(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testUser', password='testPass')
        self.refresh = str(RefreshToken.for_user(self.user))

    def test_endpoint(self):
        response = self.client.post('/users/blacklist/', {'refresh': self.refresh})
        self.assertEqual(response.status_code, 200)
