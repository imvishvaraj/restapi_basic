from rest_framework.test import APITestCase
from rest_framework import status

from rest_framework_jwt.settings import api_settings

# createing django rest framework manual token
payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER

from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse as api_reverse
# automated
# new/blank db

from postings.models import BlogPost
User = get_user_model()

class BlogPostAPITestCase(APITestCase):
    def setUp(self):
        # create test user
        user_obj = User.objects.create(username='testcfeuser', email='test@test.com')
        user_obj.set_password("somerandompassword")
        user_obj.save()

        # create test blog post
        blog_posts = BlogPost.objects.create(
            user=user_obj, 
            title='new_title', 
            content='some_random_content'
            )

    def test_single_user(self):
        #  test created user
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)

    def test_single_post(self):
        # test created blog post
        blog_count  = BlogPost.objects.count()
        self.assertEqual(blog_count, 1)

    def test_get_list(self):
        data        = {}
        url         = api_reverse("api-postings:posts")
        response    = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(response.data)

    def test_post_item_to_list_view(self):
        data        = {"title": "new_title", "content": "some more content"}
        url         = api_reverse("api-postings:posts")
        response    = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_blog_posts_get_first_item(self):
        blog_posts  = BlogPost.objects.first()
        data        = {}
        url         = blog_posts.get_api_url()
        response    = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_blog_posts_update_item(self):
        blog_posts = BlogPost.objects.first()
        url = blog_posts.get_api_url()
        data = {"title": "new_title", "content": "some more content"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_item_with_user(self):
        blog_posts  = BlogPost.objects.first()
        # print(blog_posts.content)
        url         = blog_posts.get_api_url()
        data        = {"title": "new_title2", "content": "some more content"}
        user_obj    = User.objects.first()
        payload     = payload_handler(user_obj)
        token_rsp   = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)  # JWT <token>


        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(response.data)

    def test_post_item_to_list_view_with_user(self):
        user_obj    = User.objects.first()
        payload     = payload_handler(user_obj)
        token_rsp   = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)

        data        = {"title": "new_title 3", "content": "some more content"}
        url         = api_reverse("api-postings:posts")
        response    = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_ownership(self):
        owner = User.objects.create(username='testuser2')
        blog_posts = BlogPost.objects.create(
            user=owner, 
            title='test post', 
            content='some content'
            )

        user_obj    = User.objects.first()
        self.assertNotEqual(user_obj.username, owner.username)

        payload     = payload_handler(user_obj)
        token_rsp   = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)
        url         = blog_posts.get_api_url()
        data        = {"title": "new_title mod", "content": "some more content"}
        response    = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_login(self):
        data = {
            'username': 'testcfeuser',
            'password': 'somerandompassword'
        }
        url = api_reverse("api-login")
        response = self.client.post(url, data)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get("token")
        
        if token is not None:
            blog_posts  = BlogPost.objects.first()
            # print(blog_posts.content)
            url         = blog_posts.get_api_url()
            data        = {"title": "new_title2", "content": "some more content"}
            self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)  # JWT <token>
            response = self.client.put(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
