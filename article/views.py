from django.shortcuts import render, redirect, reverse , get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from article.models import Article
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.core import serializers
from article.forms import ArticleForm
from django.contrib import messages


def full_article(request):
    return render(request, 'full_article.html')

@csrf_exempt
@require_POST
def create_article(request):
   title = request.POST.get("title")
   description = request.POST.get("description")
   image = request.FILES.get('image')  

   new_article = Article(
      title=title, description=description, image=image
   )
   new_article.save()

   return HttpResponse(b"CREATED", status=201)

def delete_article(request, id):
    article = Article.objects.get(pk = id)
    article.delete()
    return HttpResponseRedirect(reverse('article:full_article'))

def edit_article(request, id):
    # Mencari produk berdasarkan ID
    article = Article.objects.filter(pk=id).first() 

    if not article:
        # Jika produk tidak ditemukan, tampilkan pesan error
        messages.error(request, 'Produk tidak ditemukan.')
        return redirect('article:full_article')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')  

        if not title or not description:
            # Menampilkan pesan error jika field kosong
            messages.error(request, 'Silakan isi semua field terlebih dahulu.')

        else:
            # Memperbarui produk jika semua field diisi
            article.title = title
            article.description = description
            
            if image:
                article.image = image

            article.save()
            messages.success(request, 'Produk berhasil diperbarui.')
            return redirect('article:full_article')

    # Mengirim data produk ke template untuk mengisi form dengan nilai lama
    context = {
        'article':  article
    }
    return render(request, 'edit_article.html', context)

def article_detail(request, id):
    article = get_object_or_404(Article, pk=id) 
    return render(request, 'article.html', {'article': article})


def show_article(request):
   return render(request, 'full_article.html')

def show_xml(request):
   data = Article.objects.all()
   return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
   data = Article.objects.all()
   return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Article.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Article.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


