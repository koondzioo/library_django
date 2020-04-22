from django.test import TestCase
from django.urls import reverse

from catalog.models import Author


class AuthorListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        numbers_of_authors = 13

        for author_id in range(numbers_of_authors):
            Author.objects.create(
                name=f'Name {author_id}',
                surname=f'Surname {author_id}',
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/authors/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)

    def test_lists_all_authors(self):
        response = self.client.get(reverse('authors') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertTrue(len(response.context['author_list']) == 3)
        self.assertTrue(len(response.context['author_list']) == 3)

    def test_pagination(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(len(response.context['author_list']), 10)

    def test_html(self):
        response = self.client.get(reverse('authors'))
        self.assertTemplateUsed(response, 'author_list.html')
