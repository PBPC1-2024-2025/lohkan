from django.test import TestCase, Client
from article.models import Article

class BonusTddTest(TestCase):

    def test_bonus_tdd_url_is_exist(self):
        response = self.client.get('/index/')
        self.assertEqual(response.status_code, 200)

    def test_bonus_tdd_page_content(self):
        response = self.client.get('/index/')
        html_response = response.content.decode('utf8')
        self.assertIn('Try Unit Test!', html_response)



