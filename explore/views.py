from lib2to3.fixes.fix_input import context

from django.shortcuts import render, redirect
from explore.forms import FoodForm
from explore.models import Food

def show_explore(request):
    foods = Food.objects.all()

    context = {
        'test': 'test',
        'foods': foods,
    }

    return render(request, "explore.html", context)

def add_food(request):
    form = FoodForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('explore:show_explore')
    context = {'form': form}
    return render(request, "add_food.html", context)