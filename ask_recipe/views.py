from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import RecipeGroup, ChatMessage, Recipe
from .forms import RecipeGroupForm, ChatMessageForm
from django.http import HttpResponse
from django.core import serializers

def ask_recipe(request):
    groups = RecipeGroup.objects.all()  # Ambil semua grup
    return render(request, 'ask_recipe.html', {'groups': groups})

#untuk ngebuat grup resep baru
@csrf_exempt
@require_POST
def create_recipe(request):
    if request.method == "POST":
        title = request.POST.get("title")
        ingredients = request.POST.get("ingredients")
        instructions = request.POST.get("instructions")
        cooking_time = int(request.POST.get("cooking_time"))
        servings = int(request.POST.get("servings"))

        # Buat grup otomatis untuk resep ini
        group = RecipeGroup.objects.create(
            name=f"Discussion for {title}",
            description=f"Diskusi untuk resep: {title}",
            created_by=request.user
        )

        # Buat resep dan hubungkan dengan grup
        recipe = Recipe.objects.create(
            group=group,
            title=title,
            ingredients=ingredients,
            instructions=instructions,
            cooking_time=cooking_time,
            servings=servings,
            added_by=request.user
        )

        # Render HTML fragment untuk resep baru
        return render(request, 'partials/recipe_item.html', {'recipe': recipe})

    # Render halaman utama
    recipes = Recipe.objects.all()
    return render(request, 'ask_recipe.html', {'recipes': recipes})

def show_xml(request):
    data = Recipe.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Recipe.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Recipe.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Recipe.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
