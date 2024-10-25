from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.core import serializers
from explore.forms import FoodForm
from explore.models import Food
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

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
    name = request.POST.get('name')
    description = request.POST.get('description')
    min_price = request.POST.get('min_price')
    max_price = request.POST.get('max_price')
    image_link = request.POST.get('image_link')
    type = request.POST.get('type')
    user = request.user
    new_food = Food(
        name=name, description=description,
        min_price=min_price, max_price=max_price,
        image_link=image_link, type=type, user=user
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