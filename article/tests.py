from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from article.models import Article
from django.conf import settings
from django.contrib.messages import get_messages
import os
import uuid  


class TddTest(TestCase):
    # Fungsi untuk membuat data awal
    def setUp(self):
        self.client = Client()
        self.article = Article.objects.create(
            title='Test Article',
            description='Test Description'
        )
    # Fungsi mengecek apakah URL /article/ ada
    def test_bonus_tdd_url_is_exist(self):
        response = self.client.get(reverse('article:article')) 
        self.assertEqual(response.status_code, 200)  

    # Fungsi mengecek apakah template yang digunakan adalah full_article.html
    def test_article_index_template_used(self):
        response = self.client.get(reverse('article:article')) 
        self.assertTemplateUsed(response, 'full_article.html') 

    # Fungsi mengecek pembuatan article
    def test_create_article_success(self):
        data = {
            'title': 'Test Title',
            'description': 'Test Description',
        }

        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'file_content',
            content_type='image/jpeg'
        )

        response = self.client.post(
            reverse('article:create_article'),  
            data={**data, 'image': image},
            format='multipart'
        )
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content, b"CREATED")

        article = Article.objects.get(title='Test Title')
        self.assertIsNotNone(article)
        self.assertEqual(article.description, 'Test Description')
        
        file_path = os.path.join(settings.MEDIA_ROOT, article.image.name)
        self.assertTrue(os.path.exists(file_path))  

    # Fungsi mengecek apakah data artikel berhasil dihapus
    def test_delete_article_success(self):
        article_id = self.article.id  
        response = self.client.post(reverse('article:delete_article', kwargs={'id': article_id}))
        self.assertEqual(response.status_code, 302)  # 302 untuk redirect

        with self.assertRaises(Article.DoesNotExist):
            Article.objects.get(pk=article_id)

        self.assertRedirects(response, reverse('article:full_article'))

    # Fungsi mengecek apakah artikel ditemukan 
    def test_edit_article_not_found(self):
        invalid_article_id = uuid.uuid4() 
        response = self.client.post(
            reverse('article:edit_article', kwargs={'id': invalid_article_id}),
            data={'title': 'Some Title', 'description': 'Some Description'},
        )
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('Artikel tidak ditemukan.' in message.message for message in messages))

        self.assertRedirects(response, reverse('article:full_article'))

    # Fungsi mengecek apakah data artikel berhasil diubah
    def test_edit_article_incomplete_data(self):
        article_id = self.article.id 
        response = self.client.post(
            reverse('article:edit_article', kwargs={'id': article_id}),
            data={'title': '', 'description': ''},
        )

        self.assertEqual(response.status_code, 200)

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('Silakan isi semua field terlebih dahulu.' in message.message for message in messages))

        article = Article.objects.get(pk=article_id)
        self.assertEqual(article.title, 'Test Article')
        self.assertEqual(article.description, 'Test Description')

    # Fungsi mengecek data xml berhasil ditampilkan
    def test_show_xml(self):
        response = self.client.get(reverse('article:show_xml'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')
        self.assertIn('<django-objects', response.content.decode()) 
        self.assertIn('<object', response.content.decode())  
        self.assertIn(f'pk="{self.article.id}"', response.content.decode())  
        self.assertIn('<field name="title"', response.content.decode())  
        self.assertIn('<field name="description"', response.content.decode()) 

    # Fungsi mengecek data json berhasil ditampilkan
    def test_show_json(self):
        response = self.client.get(reverse('article:show_json'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertIn('"pk":', response.content.decode())  

    # Fungsi mengecek data xml berhasil ditampilkan berdasarkan id
    def test_show_xml_by_id(self):
        response = self.client.get(reverse('article:show_xml_by_id', kwargs={'id': self.article.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')
        self.assertIn('<django-objects', response.content.decode())
        self.assertIn(f'pk="{self.article.id}"', response.content.decode())  

    # Fungsi mengecek data json berhasil ditampilkan berdasarkan id
    def test_show_json_by_id(self):
        response = self.client.get(reverse('article:show_json_by_id', kwargs={'id': self.article.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertIn('"pk":', response.content.decode())
