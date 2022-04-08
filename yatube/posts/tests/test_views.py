from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post

User = get_user_model()


class PostsViewsTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')

        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Текстовое описание',
        )
        cls.post_user = Post.objects.create(
            author=cls.user,
            text='Тестовый пост User',
            group=cls.group,
        )

        cls.index_reverse = reverse('posts:index')
        cls.group_list_reverse = reverse(
            'posts:group_list', kwargs={'slug': 'test-slug'}
        )
        cls.profile_reverse = reverse(
            'posts:profile', kwargs={'username': 'auth'}
        )
        cls.post_detail_reverse = reverse(
            'posts:post_detail', kwargs={'post_id': str(cls.post_user.pk)}
        )
        cls.create_post_reverse = reverse('posts:post_create')
        cls.edit_post_reverse = reverse(
            'posts:post_edit', kwargs={'post_id': str(cls.post_user.pk)}
        )

        cls.pages_names = (
            ('posts/index.html', cls.index_reverse),
            ('posts/profile.html', cls.profile_reverse),
            ('posts/create_and_edit_post.html', cls.create_post_reverse),
            ('posts/create_and_edit_post.html', cls.edit_post_reverse),
            ('posts/group_list.html', cls.group_list_reverse),
            ('posts/post_detail.html', cls.post_detail_reverse),
        )

    def setUp(self) -> None:
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        templates_pages_names = self.pages_names
        for template, reverse_name in templates_pages_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_post_edit_page_uses_correct_template(self):
        response = self.authorized_client.get(self.edit_post_reverse)
        self.assertTemplateUsed(response, 'posts/create_and_edit_post.html')

    def test_index_page_show_correct_context(self):
        response = self.guest_client.get(self.index_reverse)
        first_object = response.context['page_obj'][0]
        self.context_test(first_object)

    def test_posts_group_list_correct_context(self):
        response = self.guest_client.get(self.group_list_reverse)
        self.assertEqual(
            response.context.get('group').title, self.group.title
        )
        self.assertEqual(
            response.context.get('group').description, self.group.description
        )

        first_object = response.context['page_obj'][0]
        self.context_test(first_object)

    def test_profile_correct_context(self):
        response = self.guest_client.get(self.profile_reverse)
        self.assertEqual(
            response.context.get('author').username, self.user.username
        )
        first_object = response.context['page_obj'][0]
        self.context_test(first_object)

    def test_post_detail_correct_context(self):
        response = self.guest_client.get(self.post_detail_reverse)
        self.assertEqual(
            response.context.get('post').text, self.post_user.text
        )

        first_object = response.context['post']
        self.context_test(first_object)

    def test_post_create_correct_context(self):
        response = self.authorized_client.get(self.create_post_reverse)

        from_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

        for value, expected in from_fields.items():
            with self.subTest(value=value):
                from_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(from_field, expected)

    def test_post_edit_correct_context(self):
        response = self.authorized_client.get(self.edit_post_reverse)

        from_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

        for value, expected in from_fields.items():
            with self.subTest(value=value):
                from_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(from_field, expected)

    def context_test(self, post_user_obj):
        text = post_user_obj.text
        author = post_user_obj.author.username
        group = post_user_obj.group.title

        self.assertEqual(text, self.post_user.text)
        self.assertEqual(author, self.post_user.author.username)
        self.assertEqual(group, self.group.title)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.count_posts = settings.PAGE_SIZE
        cls.count_posts_list_two = settings.PAGE_SIZE // 2

        cls.user = User.objects.create_user(username='auth')

        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Текстовое описание',
        )

        for i in range(cls.count_posts + cls.count_posts_list_two):
            Post.objects.create(
                author=cls.user,
                text='Тестовый пост User',
                group=cls.group,
            )

        cls.reverse_contains_posts = (
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': 'test-slug'}),
            reverse('posts:profile', kwargs={'username': 'auth'})
        )

    def setUp(self) -> None:
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_first_contains_posts(self):
        templates_contains_posts = self.reverse_contains_posts
        for template in templates_contains_posts:
            with self.subTest(adress=template):
                response = self.authorized_client.get(
                    template
                )
                self.assertEqual(
                    len(response.context['page_obj']), self.count_posts
                )

    def test_second_contains_posts(self):
        templates_contains_posts = self.reverse_contains_posts
        for template in templates_contains_posts:
            template = template + '?page=2'
            with self.subTest(adress=template):
                response = self.authorized_client.get(template)
                self.assertEqual(
                    len(
                        response.context['page_obj']),
                    self.count_posts_list_two
                )


class PostIntegrationViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')

        cls.group_firs = Group.objects.create(
            title='Тестовая группа 1',
            slug='test-slug-1',
            description='Текстовое описание 1',
        )

        cls.group_second = Group.objects.create(
            title='Тестовая группа 2',
            slug='test-slug-2',
            description='Текстовое описание 2',
        )

        cls.post_user = Post.objects.create(
            author=cls.user,
            text='Тестовый пост User',
            group=cls.group_firs,
        )

    def setUp(self) -> None:
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_group_test_of_created_post(self):
        response_index = self.authorized_client.get(reverse('posts:index'))
        response_group = self.authorized_client.get(
            reverse('posts:group_list',
                    kwargs={'slug': 'test-slug-1'})
        )
        response_profile = self.authorized_client.get(
            reverse('posts:profile',
                    kwargs={'username': 'auth'})
        )

        self.assertEqual(
            response_index.context['page_obj'][0].text,
            self.post_user.text
        )
        self.assertEqual(
            response_index.context['page_obj'][0].group.title,
            self.group_firs.title
        )
        self.assertIsNot(
            response_index.context['page_obj'][0].group.title,
            self.group_second.title
        )
        self.assertEqual(
            response_group.context['page_obj'][0].text,
            self.post_user.text
        )
        self.assertEqual(
            response_profile.context['page_obj'][0].text,
            self.post_user.text
        )
