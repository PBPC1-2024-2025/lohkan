from django.shortcuts import render, redirect, reverse, get_object_or_404
from bucket_list.forms import BucketListForm
from bucket_list.models import BucketList
from explore.models import Food
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required

@csrf_exempt
@require_POST
def add_bucket_list(request):
    user = request.user
    name = strip_tags(request.POST.get('name'))
    
    new_bucket_list = BucketList(user=user, name=name)
    new_bucket_list.save()
    
    return HttpResponse(b"CREATED", status=201)

@csrf_exempt
def edit_bucket_list(request, id):
    bucket_list = BucketList.objects.get(pk=id)
    form = BucketListForm(request.POST or None, instance=bucket_list)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('bucket_list:show_bucket_list'))

    # context = {'form': form}
    return JsonResponse({'status': 'false'})

def delete_bucket_list(request, id):
    bucket_list = BucketList.objects.get(pk=id)
    bucket_list.delete()
    return HttpResponseRedirect(reverse('bucket_list:show_bucket_list'))

@login_required
def show_bucket_list(request):
    return render(request, "bucket_list.html")

@login_required
def show_bucket_list_history(request):
    return render(request, "bucket_list_history.html")

def show_json(request):
    data = BucketList.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def get_food(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    food_data = {
        'id': str(food.id),
        'name': food.name,
        'description': food.description,
        'min_price': food.min_price,
        'max_price': food.max_price,
        'image_link': food.image_link,
        'type': food.type,
    }
    return JsonResponse(food_data)

@csrf_exempt
def remove_from_bucket_list(request, food_id, bucket_id):
    try:
        # Try to get the bucket list
        try:
            bucket = BucketList.objects.get(id=bucket_id, user=request.user)
        except BucketList.DoesNotExist:
            return JsonResponse(
                {'success': False, 'error': 'Bucket list not found'}, 
                status=404
            )

        # Try to get the food item
        try:
            food = Food.objects.get(id=food_id)
        except Food.DoesNotExist:
            return JsonResponse(
                {'success': False, 'error': 'Food item not found'}, 
                status=404
            )
        bucket.foods.remove(food)
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)