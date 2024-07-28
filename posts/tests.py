from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Post, Comment


# Create your tests here.
class TestSetup(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='testUser', password='testPass')
        self.post = Post.objects.create(content='testContent', author=self.user)
        self.comment = Comment.objects.create(content='testComment', post=self.post, author=self.user)


class PostTestCase(TestSetup):
    def test_post(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, 200, 'Status code is not 200')
        self.assertEqual(response.data[0]['content'], 'testContent', 'Content is not testContent')
        self.client.force_authenticate(user=None)

    def test_post_create(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/posts/', {'content': 'newContent'})
        self.assertEqual(response.status_code, 201, 'Status code is not 201')
        self.assertEqual(response.data['content'], 'newContent', 'Content is not newContent')
        self.client.force_authenticate(user=None)

    def test_post_update(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(f'/posts/{self.post.id}/', {'content': 'updatedContent'})
        self.assertEqual(response.status_code, 200, 'Status code is not 200')
        self.assertEqual(response.data['content'], 'updatedContent', 'Content is not updatedContent')
        self.client.force_authenticate(user=None)

    def test_post_delete(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/posts/{self.post.id}/')
        self.assertEqual(response.status_code, 204, 'Status code is not 204')
        self.client.force_authenticate(user=None)

    def test_post_search(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/posts/?search=testContent')
        self.assertEqual(response.status_code, 200, 'Status code is not 200')
        self.assertEqual(response.data[0]['content'], 'testContent', 'Content is not testContent')
        self.client.force_authenticate(user=None)

    def test_post_search_no_result(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/posts/?search=noResult')
        self.assertEqual(response.status_code, 200, 'Status code is not 200')
        self.assertEqual(len(response.data), 0, 'Response is not empty')
        self.client.force_authenticate(user=None)

    def test_post_create_unauthenticated(self):
        response = self.client.post('/posts/', {'content': 'newContent'})
        self.assertEqual(response.status_code, 403, 'Status code is not 403')

    def test_post_update_not_author(self):
        user2 = User.objects.create(username='testUser2', password='testPass')
        self.client.force_authenticate(user=user2)
        response = self.client.put(f'/posts/{self.post.id}/', {'content': 'updatedContent'})
        self.assertEqual(response.status_code, 403, 'Status code is not 403')
        self.client.force_authenticate(user=None)


class CommentTestCase(TestSetup):
    def test_comment(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/posts/{self.post.id}/comments/')
        self.assertEqual(response.status_code, 200, 'Status code is not 200')
        self.assertEqual(response.data[0]['content'], 'testComment', 'Content is not testComment')
        self.client.force_authenticate(user=None)

    def test_comment_create(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f'/posts/{self.post.id}/comments/', {'content': 'newComment'})
        self.assertEqual(response.status_code, 201, 'Status code is not 201')
        self.assertEqual(response.data['content'], 'newComment', 'Content is not newComment')
        self.client.force_authenticate(user=None)

    def test_comment_update(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(f'/posts/{self.post.id}/comments/{self.comment.id}/', {'content': 'updatedComment'})
        self.assertEqual(response.status_code, 200, 'Status code is not 200')
        self.assertEqual(response.data['content'], 'updatedComment', 'Content is not updatedComment')
        self.client.force_authenticate(user=None)

    def test_comment_delete(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/posts/{self.post.id}/comments/{self.comment.id}/')
        self.assertEqual(response.status_code, 204, 'Status code is not 204')
        self.client.force_authenticate(user=None)

    def test_comment_search(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/posts/{self.post.id}/comments/?search=testComment')
        self.assertEqual(response.status_code, 200, 'Status code is not 200')
        self.assertEqual(response.data[0]['content'], 'testComment', 'Content is not testComment')
        self.client.force_authenticate(user=None)

    def test_comment_search_no_result(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/posts/{self.post.id}/comments/?search=noResult')
        self.assertEqual(response.status_code, 200, 'Status code is not 200')
        self.assertEqual(len(response.data), 0, 'Response is not empty')
        self.client.force_authenticate(user=None)

    def test_comment_create_unauthenticated(self):
        response = self.client.post(f'/posts/{self.post.id}/comments/', {'content': 'newComment'})
        self.assertEqual(response.status_code, 403, 'Status code is not 403')

    def test_comment_update_not_author(self):
        user2 = User.objects.create(username='testUser2', password='testPass')
        self.client.force_authenticate(user=user2)
        response = self.client.put(f'/posts/{self.post.id}/comments/{self.comment.id}/', {'content': 'updatedComment'})
        self.assertEqual(response.status_code, 403, 'Status code is not 403')
        self.client.force_authenticate(user=None)


class LikeTestCase(TestSetup):
    def test_post_like(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f'/posts/{self.post.id}/like/')
        self.assertEqual(response.status_code, 201, 'Status code is not 201')
        self.assertEqual(response.data['likes'], 1, 'Likes is not 1')
        self.client.force_authenticate(user=None)

    # def test_post_unlike(self):
    #     self.client.force_authenticate(user=self.user)
    #     self.client.post(f'/posts/{self.post.id}/like/')
    #     response = self.client.post(f'/posts/{self.post.id}/like/')
    #     self.assertEqual(response.status_code, 204, 'Status code is not 204')
    #     self.assertEqual(response.data['likes'], 0, 'Likes is not 0')
    #     self.client.force_authenticate(user=None)
    #
    # def test_comment_like(self):
    #     self.client.force_authenticate(user=self.user)
    #     response = self.client.post(f'/posts/{self.post.id}/comments/{self.comment.id}/like/')
    #     self.assertEqual(response.status_code, 201, 'Status code is not 201')
    #     self.assertEqual(response.data['likes'], 1, 'Likes is not 1')
    #     self.client.force_authenticate(user=None)
    #
    # def test_comment_unlike(self):
    #     self.client.force_authenticate(user=self.user)
    #     self.client.post(f'/posts/{self.post.id}/comments/{self.comment.id}/like/')
    #     response = self.client.post(f'/posts/{self.post.id}/comments/{self.comment.id}/like/')
    #     self.assertEqual(response.status_code, 204, 'Status code is not 204')
    #     self.assertEqual(response.data['likes'], 0, 'Likes is not 0')
    #     self.client.force_authenticate(user=None)
    #
    # def test_post_like_unauthenticated(self):
    #     response = self.client.post(f'/posts/{self.post.id}/like/')
    #     self.assertEqual(response.status_code, 401, 'Status code is not 401')
    #
    # def test_comment_like_unauthenticated(self):
    #     response = self.client.post(f'/posts/{self.post.id}/comments/{self.comment.id}/like/')
    #     self.assertEqual(response.status_code, 401, 'Status code is not 401')
    #
    # def test_post_unlike_unauthenticated(self):
    #     response = self.client.post(f'/posts/{self.post.id}/like/')
    #     self.assertEqual(response.status_code, 401, 'Status code is not 401')
    #
    # def test_comment_unlike_unauthenticated(self):
    #     response = self.client.post(f'/posts/{self.post.id}/comments/{self.comment.id}/like/')
    #     self.assertEqual(response.status_code, 401, 'Status code is not 401')
