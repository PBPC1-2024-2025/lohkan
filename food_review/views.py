from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from food_review.models import ReviewEntry
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.db.models import Count
# from article.forms import ArticleForm
# from django.contrib import messages

# menampilkan semua review
def page_review(request):
    # Aggregate reviews and count each unique food name
    food_type_filter = request.GET.get('type', 'All')
    search_query = request.GET.get('search', '').strip()  # Get search query
    
    if search_query:  # If there is a search query
        reviews = (ReviewEntry.objects
                   .filter(name__icontains=search_query)  # Case-insensitive search
                   .values('name', 'food_type')
                   .annotate(review_count=Count('id'))
                   .order_by('name'))
    else:
        if food_type_filter != 'All':
            reviews = (ReviewEntry.objects.filter(food_type=food_type_filter)
                       .values('name', 'food_type')
                       .annotate(review_count=Count('id'))
                       .order_by('name'))
        else:
            reviews = (ReviewEntry.objects
                       .values('name', 'food_type')
                       .annotate(review_count=Count('id'))
                       .order_by('name'))


    return render(request, 'page_review.html', {'reviews': reviews})

# membuat review baru

@login_required  # If using user authentication
@csrf_exempt
@require_POST
def add_review_ajax(request):
    raw_name = request.POST.get('name').strip()  # Get the raw name input
    name = raw_name.lower()  # Normalize name to lowercase for comparison
    food_type = request.POST.get('food_type')
    rating = request.POST.get('rating')
    comments = request.POST.get('comments')
    user = request.user  # Assuming you are using Django's authentication

    # Check if the review already exists for the same normalized food item and type
    existing_review = ReviewEntry.objects.filter(name__iexact=raw_name, food_type=food_type, user=user).first()
    if existing_review:
        # If existing, update the existing review
        existing_review.rating = rating
        existing_review.comments = comments
        existing_review.save()
        return HttpResponse(b"UPDATED", status=200)  # Changed response for clarity
    else:
        # If not existing, create a new review
        new_review = ReviewEntry(
            name=raw_name.title(),  # Store name in title case
            food_type=food_type,
            rating=rating,
            comments=comments,
            user=user
        )
        new_review.save()
        return HttpResponse(b"CREATED", status=201)

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


def see_reviews(request, food_name, food_type):
   # Fetch all reviews for the given food name and type
    reviews = ReviewEntry.objects.filter(name=food_name, food_type=food_type).select_related('user')
    return render(request, 'see_reviews.html', {'reviews': reviews, 'food_name': food_name, 'food_type': food_type})