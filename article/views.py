from django.shortcuts import render, redirect, reverse , get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from article.models import Article, Comment
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.core import serializers
from django.contrib import messages
from django.core.paginator import Paginator

# menampilkan semua artikel
def full_article(request):
    article_list = Article.objects.all().order_by('-id')
    return render(request, 'full_article.html', {'article_list': article_list})

# membuat artikel baru
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

# menghapus artikel
def delete_article(request, id):
    article = Article.objects.get(pk = id)
    article.delete()
    return HttpResponseRedirect(reverse('article:full_article'))

# mengedit artikel
def edit_article(request, id):
    article = Article.objects.filter(pk=id).first() 
    if not article:
        messages.error(request, 'Article not found.')
        return redirect('article:full_article')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')  

        if not title or not description:
            messages.error(request, 'Please fill in all fields first.')

        else:
            article.title = title
            article.description = description
            
            if image:
                article.image = image

            article.save()
            messages.success(request, 'Article successfully updated.')
            return redirect('article:full_article')
        
    context = {
        'article':  article
    }
    return render(request, 'edit_article.html', context)

# menampilkan detail artikel
def article_detail(request, id):
    article = get_object_or_404(Article, pk=id)
    comments = Comment.objects.filter(article=article).order_by('-created_at') 
    return render(request, 'article.html', {'article': article, 'comments': comments})


def add_comment(request, id):  
    article = get_object_or_404(Article, pk=id) 
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(article=article, content=content, user=request.user)
            return redirect('article:article_detail', id=id)  
    return redirect('article:article_detail', id=id)


# menampilkan artikel dalam format JSON
def show_xml(request):
   data = Article.objects.all()
   return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

# menampilkan artikel berdasarkan id dalam format XML
def show_json(request):
   data = Article.objects.all()
   return HttpResponse(serializers.serialize("json", data), content_type="application/json")

# menampilkan artikel berdasarkan id dalam format JSON
def show_xml_by_id(request, id):
    data = Article.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

# menampilkan artikel berdasarkan id dalam format JSON
def show_json_by_id(request, id):
    data = Article.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def index(request):
    return render(request, 'full_article.html')