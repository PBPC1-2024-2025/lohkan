from django.test import TestCase, Client

class BonusTddTest(TestCase):

    def test_bonus_tdd_url_is_exist(self):
        response = Client().get('/article')
        self.assertEqual(response.status_code,200)

    def test_bonus_tdd_page_content(self):
        response = Client().get('/article')
        html_response = response.content.decode('utf8')
        self.assertIn('title', html_response)



