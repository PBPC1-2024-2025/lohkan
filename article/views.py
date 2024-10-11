from django.shortcuts import render, redirect, reverse , get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from article.models import Article
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.core import serializers
from article.forms import ArticleForm


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
    article = Article.objects.get(pk = id)
    form = ArticleForm(request.POST or None, instance=article)
    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('article:full_article'))
    context = {'form': form}
    return render(request, "edit_article.html", context)

def detail_article(request, id):
    article = get_object_or_404(Article, pk=id)
    return render(request, 'article.html', {
        'title': article.title,
        'description': article.description,
        'image': article.image,
    })

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


