from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse_lazy

from ..models import Group, Post

User = get_user_model()


class PostsURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.author = User.objects.create_user(
            username='author',
            email='author@author.ru',
            password='123456_password',
        )
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post_user = Post.objects.create(
            author=cls.user,
            text='Тестовый пост User',
        )
        cls.post_author = Post.objects.create(
            author=cls.author,
            text='Тестовый пост Author',
        )
        cls.index_url = '/'
        cls.group_list_url = f'/group/{cls.group.slug}/'
        cls.profile_url = f'/profile/{cls.author.username}/'
        cls.post_detail_url = f'/posts/{cls.post_user.id}/'
        cls.create_post_url = '/create/'
        cls.edit_post_url = f'/posts/{cls.post_user.id}/edit/'
        cls.unexisting_page_url = '/unexisting_page/'

        cls.public_urls = {
            cls.index_url: 'posts/index.html',
            cls.group_list_url: 'posts/group_list.html',
            cls.profile_url: 'posts/profile.html',
            cls.post_detail_url: 'posts/post_detail.html',
        }

        cls.private_urls = {
            cls.create_post_url: 'posts/create_and_edit_post.html',
            cls.edit_post_url: 'posts/create_and_edit_post.html',
        }

    def setUp(self) -> None:
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.author_client = Client()
        self.author_client.force_login(self.author)

    def test_public_url_exists_at_desired_location(self):
        templates_url_names = self.public_urls
        for template_key, address_value in templates_url_names.items():
            with self.subTest(adress=template_key):
                response = self.authorized_client.get(template_key)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_not_existed_location(self):
        response = self.guest_client.get(self.unexisting_page_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_create_and_edit_post_url_exists_at_desired_location(self):
        response = self.authorized_client.get(self.create_post_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_private_url_redirect_guest_on_login(self):
        for address in self.private_urls:
            with self.subTest(address=address):
                response = self.guest_client.get(address, follow=True)
                reverse_page = reverse_lazy('users:login')
                self.assertRedirects(response,
                                     f'{reverse_page}?next={address}')

    def test_post_url_edit_exists_at_desired_location(self):
        post_edit_author_url = self.post_detail_url
        response = self.author_client.get(post_edit_author_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_uses_correct_template(self):
        templates_url_names = {**self.public_urls, **self.private_urls}
        for template_key, address_value in templates_url_names.items():
            with self.subTest(adress=template_key):
                response = self.authorized_client.get(template_key)
                self.assertTemplateUsed(response, address_value)
