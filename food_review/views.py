import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from food_review.models import ReviewEntry
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg


# menampilkan semua review
def page_review(request):
    # Aggregate reviews and count each unique food name
    food_type_filter = request.GET.get('type', 'All')
    search_query = request.GET.get('search', '').strip()
    
    if search_query:
        reviews = (ReviewEntry.objects
                   .filter(name__icontains=search_query)
                   .values('name', 'food_type')
                   .annotate(review_count=Count('id'), avg_rating=Avg('rating'))
                   .order_by('-avg_rating', 'name'))
    else:
        if food_type_filter != 'All':
            reviews = (ReviewEntry.objects.filter(food_type=food_type_filter)
                       .values('name', 'food_type')
                       .annotate(review_count=Count('id'), avg_rating=Avg('rating'))
                       .order_by('-avg_rating', 'name'))
        else:
            reviews = (ReviewEntry.objects
                       .values('name', 'food_type')
                       .annotate(review_count=Count('id'), avg_rating=Avg('rating'))
                       .order_by('-avg_rating', 'name'))

    # Fetch top 3 rated dishes independently of search or filters
    top_rated_dishes = (ReviewEntry.objects
                        .values('name', 'food_type')
                        .annotate(review_count=Count('id'), avg_rating=Avg('rating'))
                        .order_by('-avg_rating', 'name')[:3])

    return render(request, 'page_review.html', {
        'reviews': reviews,
        'top_rated_dishes': top_rated_dishes
    })

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

def see_reviews(request, food_name, food_type='unknown'):
    reviews = ReviewEntry.objects.filter(name=food_name, food_type=food_type).select_related('user')
    if reviews.exists():
        average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        rating_label = get_rating_label(average_rating)

        if request.GET.get('format') == 'json':
            # Including username in the JSON output
            reviews_data = [{
                'username': review.user.username,
                'rating': review.rating,
                'comments': review.comments
            } for review in reviews]
            return JsonResponse({
                'reviews': reviews_data,
                'average_rating': average_rating,
                'rating_label': rating_label
            })
        else:
            return render(request, 'see_reviews.html', {
                'reviews': reviews,
                'food_name': food_name,
                'food_type': food_type,
                'average_rating': average_rating,
                'rating_label': rating_label
            })
    else:
        if request.GET.get('format') == 'json':
            return JsonResponse({'message': 'No reviews found'}, status=404)
        else:
            return render(request, 'see_reviews.html', {
                'reviews': [],
                'food_name': food_name,
                'food_type': food_type,
                'average_rating': 0,
                'rating_label': "No reviews yet. 😢"
            })

def get_rating_label(average_rating):
    if average_rating <= 2:
        return "Not quite good 🤔"
    elif 2 < average_rating <= 3:
        return "Maybe later 😬"
    elif 3 < average_rating <= 4:
        return "Maybe try some 😄"
    else:
        return "Recommended! 🤤"


@csrf_exempt
def create_review_flutter(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        
        new_review = ReviewEntry.objects.create(
            user=request.user,
            food_name=data["food_name"],
            food_type = data["food_type"],
            rating=int(data["rating"]),
            comments=data["comments"],
        )

        new_review.save()

        return JsonResponse({"status": "success"}, status=201)
    else:
        return JsonResponse({"status": "error"}, status=401)