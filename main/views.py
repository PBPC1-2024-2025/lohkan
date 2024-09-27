from django.shortcuts import render, redirect
from main.forms import FoodEntryForm
from main.models import FoodEntry
from django.http import HttpResponse
from django.core import serializers


def show_main(request):
    food_entries = FoodEntry.objects.all()

    context = {
        'nama': 'admin',
        'deskripsi': 'lorem ipsum',
        'harga': '20000',
        'food_entries': food_entries,  
    }

    return render(request, "main.html", context)


def create_food_entry(request):
    form = FoodEntryForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_food_entry.html", context)

def show_xml(request):
    data = FoodEntry.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = FoodEntry.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = FoodEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = FoodEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")