from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый сдаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Т' * 30,
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str___."""
        group = PostModelTest.group
        post = PostModelTest.post
        self.assertEqual(group.title, str(group))
        self.assertEqual(post.text[:15], str(post))

    def test_group_verbose_name(self):
        group = PostModelTest.group
        group_field_verboses = {
            'title': 'Наименование группы',
            'slug': 'Ссылка',
            'description': 'Описание группы',
        }

        for field, expected_value in group_field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    group._meta.get_field(field).verbose_name, expected_value
                )

    def test_post_verbose_name(self):
        post = PostModelTest.post
        post_field_verboses = {
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Ссылка группы',
        }

        for field, expected_value in post_field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected_value
                )

    def test_group_help_text(self):
        group = PostModelTest.group
        group_field_help_text = {
            'title': 'Наименование группы',
            'slug': 'Ссылка на группу',
            'description': 'Описание группы',
        }

        for field, expected_value in group_field_help_text.items():
            with self.subTest(field=field):
                self.assertEqual(
                    group._meta.get_field(field).help_text, expected_value
                )

    def test_post_help_text(self):
        post = PostModelTest.post
        post_field_help_text = {
            'text': 'Введите текст поста',
            'pub_date': 'Дата публикации поста',
            'author': 'Автор поста',
            'group': 'Группа, к которой будет относиться пост',
        }

        for field, expected_value in post_field_help_text.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text, expected_value
                )
