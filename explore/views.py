from lib2to3.fixes.fix_input import context

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.core import serializers

from explore.forms import FoodForm
from explore.models import Food

@login_required(login_url='auth/login')
def show_explore(request):
    foods = Food.objects.all()
    user = request.user
    context = {
        'foods': foods,
        'user': user
    }
    return render(request, "explore.html", context)

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