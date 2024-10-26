from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from explore.models import Food


@csrf_exempt
@require_POST
def add_food_ajax(request):
    name = request.POST.get('name')
    description = request.POST.get('description')
    min_price = request.POST.get('min_price')
    max_price = request.POST.get('max_price')

    new_food = Food(name=name, description=description, min_price=min_price, max_price=max_price)
    new_food.save()
    return HttpResponse(b"CREATED", status= 201)


