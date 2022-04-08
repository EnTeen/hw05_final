from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Post, User

User = get_user_model()


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый текст',
        )

    def setUp(self) -> None:
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_new_post_created_in_database(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Текст для теста',
        }
        self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        post = Post.objects.first()
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertEqual(post.text,
                         form_data['text'])
        self.assertEqual(post.author.username,
                         self.post.author.username)
        self.assertIsNone(post.group)

    def test_post_edited_in_database(self):
        posts_count = Post.objects.count()
        post_id = self.post.pk
        form_data_edited = {
            'text': 'Отредактированный текст для теста',
        }
        self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': post_id}),
            data=form_data_edited,
            follow=True
        )
        post = Post.objects.first()
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertTrue(Post.objects.filter(
            text=form_data_edited.get('text')).exists())
        self.assertNotEqual(post.text,
                            self.post.text)
        self.assertEqual(post.author.username,
                         self.post.author.username)
