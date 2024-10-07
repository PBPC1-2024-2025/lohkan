from django.shortcuts import render, redirect
from article.models import Article
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.core import serializers


def full_article(request):
    return render(request, 'full_article.html')

@csrf_exempt
@require_POST
def create_article(request):
   title = request.POST.get("mood")
   description = request.POST.get("feelings")
   image = request.FILES.get('image')  
   user = request.user

   new_article = Article(
      title=title, description=description, image=image,
      user=user
   )
   new_article.save()

   return HttpResponse(b"CREATED", status=201)

def show_article(request):
    
   context = {
     
   }
   return render(request, 'full_article.html', context)

def show_xml(request):
    data = Article.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Article.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


