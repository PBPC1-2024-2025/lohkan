from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse
from django.core import serializers
from explore.forms import FoodForm
from explore.models import Food
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
import json

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
    # foods = Food.objects.all()
    user = request.user
    context = {
        # 'foods': foods,
        'user': user
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