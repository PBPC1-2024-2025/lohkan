from pydoc import describe

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.core import serializers
from explore.forms import FoodForm, CsvForm
from explore.models import Food, Csv
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
import json
from bucket_list.models import BucketList
import json, csv

def upload_file(request):
    form = CsvForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        obj = Csv.objects.get(activated=False)
        with open(obj.file_name.path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            for i, row in enumerate(reader):
                if i==0:
                    pass
                else:
                    name = row[0]
                    description = row[1]
                    min_price = row[2]
                    max_price = row[3]
                    type = row[4]
                    image_link = row[5]
                    Food.objects.create(name=name, description=description, min_price=min_price, max_price=max_price, image_link=image_link, type=type)
                    print(row)
        obj.activated = True
        obj.save()
        form = CsvForm()
        return HttpResponseRedirect(reverse('explore:show_explore'))
    return render(request, 'upload_file.html', {'form': form})

def all_to_json(request):
    if request.method == 'POST':
        foods = Food.objects.all()
        data = foods.values()
        return JsonResponse(list(data), safe=False)

def search_food(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        foods = Food.objects.filter(
            name__icontains=search_str
        )
        data = foods.values()
        return JsonResponse(list(data), safe=False)

def filter_food(request):
    if request.method == 'POST':
        selected_type = json.loads(request.body).get('selectedType')
        foods = Food.objects.filter(
            type__iexact=selected_type
        )
        data = foods.values()
        return JsonResponse(list(data), safe=False)

@login_required(login_url='auth/login')
def show_explore(request):
    foods = Food.objects.all()
    bucket_lists = BucketList.objects.filter(user=request.user)    # buat dropdown
    user = request.user
    context = {
        'foods': foods,
        'bucket_lists': bucket_lists,    # context
        'user': user,
    }
    return render(request, "explore.html", context)

@csrf_exempt
@require_POST
def add_food_ajax(request):
    name = strip_tags(request.POST.get('name'))
    description = strip_tags(request.POST.get('description'))
    min_price = request.POST.get('min_price')
    max_price = request.POST.get('max_price')
    image_link = request.POST.get('image_link')
    type = request.POST.get('type')
    new_food = Food(
        name=name, description=description,
        min_price=min_price, max_price=max_price,
        image_link=image_link, type=type
    )
    new_food.save()
    return HttpResponse(b"CREATED", status=201)

def add_food(request):
    form = FoodForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('explore:show_explore')
    context = {'form': form}
    return render(request, "add_food.html", context)

@csrf_exempt
def add_food_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_food = Food.objects.create(
            name=data['name'],
            description=data['description'],
            min_price=int(data['min_price']),
            max_price=int(data['max_price']),
            image_link=data['image_link'],
            type=data['type']
        )
        new_food.save()
        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)

def edit_food(request, id):
    food = Food.objects.get(pk=id)
    form = FoodForm(request.POST or None, instance=food)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return HttpResponseRedirect(reverse('explore:show_explore'))
    context = {'form': form}
    return render(request, "edit_food.html", context)

def delete_food(request, id):
    food = Food.objects.get(pk=id)
    food.delete()
    return HttpResponseRedirect(reverse('explore:show_explore'))

def show_xml(request):
    data = Food.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Food.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

# bismillah
def add_to_bucket_list(request, food_id, bucket_id):
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
        bucket.foods.add(food)
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)