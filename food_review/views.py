from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from food_review.models import ReviewEntry
from django.core import serializers
# from article.forms import ArticleForm
# from django.contrib import messages

# menampilkan semua review
def page_review(request):
    return render(request, 'page_review.html')

# membuat review baru
@csrf_exempt
@require_POST
def add_review_ajax(request):
    name = request.POST.get('name')
    food_type = request.POST.get('food_type')
    rating = request.POST.get('rating')
    comments = request.POST.get('comments')

    new_review = ReviewEntry(name=name, food_type=food_type, rating=rating, comments=comments)
    new_review.save()
    return HttpResponse(b"CREATED", status= 201)

# menampilkan artikel dalam format JSON
def show_xml(request):
   data = ReviewEntry.objects.all()
   return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

# menampilkan artikel berdasarkan id dalam format XML
def show_json(request):
   data = ReviewEntry.objects.all()
   return HttpResponse(serializers.serialize("json", data), content_type="application/json")

# menampilkan artikel berdasarkan id dalam format JSON
def show_xml_by_id(request, id):
    data = ReviewEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

# menampilkan artikel berdasarkan id dalam format JSON
def show_json_by_id(request, id):
    data = ReviewEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def index(request):
    return render(request, 'page_review.html')