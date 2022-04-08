from http import HTTPStatus

from django.test import TestCase


class ViewTestClass(TestCase):
    def test_error_page_404(self):
        response = self.client.get('/nonexist-page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateUsed(response, 'core/404.html')

    def test_permission_denied(self):
        response = self.client.get('/403/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateUsed(response, 'core/403.html')

    def test_server_error(self):
        response = self.client.get('/500/')
        self.assertEqual(response.status_code, 500)
        self.assertTemplateUsed(response, 'core/500.html')
