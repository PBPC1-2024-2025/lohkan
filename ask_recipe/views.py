import json
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import RecipeGroup, ChatMessage, Recipe
from .forms import RecipeForm
from django.http import Http404, HttpResponse, JsonResponse
from django.core import serializers
from django.contrib import messages

def ask_recipe(request):
    # ngambil semua resep dari database
    recipes = Recipe.objects.all()
    return render(request, 'ask_recipe.html', {'recipes': recipes})

#untuk ngebuat grup resep baru
@csrf_exempt
@require_POST
def create_recipe(request):
    if request.method == "POST":
        try:
            # Get data from post request
            title = request.POST.get("title")
            ingredients = request.POST.get("ingredients")
            instructions = request.POST.get("instructions")
            cooking_time = int(request.POST.get("cooking_time"))
            servings = int(request.POST.get("servings"))

            # Validate required data
            if not title or not ingredients or not instructions or not cooking_time or not servings:
                return HttpResponse("All fields are required", status=400)

            # Normalize the title (remove extra spaces and convert to lowercase)
            normalized_title = ' '.join(title.lower().split())
            
            # Check for existing recipes with normalized names
            existing_recipes = Recipe.objects.all()
            for existing_recipe in existing_recipes:
                existing_normalized_title = ' '.join(existing_recipe.title.lower().split())
                if normalized_title == existing_normalized_title:
                    return HttpResponse(
                        f"Recipe with the name '{title}' already exists.", 
                        status=400
                    )

            # Create group first
            group_name = f"Discussion for {title}"
            group = RecipeGroup.objects.create(
                name=group_name,
                description=f"Discussion group for {title}",
                created_by=request.user
            )

            # Then create recipe with the group reference
            recipe = Recipe.objects.create(
                title=title,
                ingredients=ingredients,
                instructions=instructions,
                cooking_time=cooking_time, 
                servings=servings,
                added_by=request.user,
                group=group
            )

            # Update the group with the recipe reference if needed
            group.recipe = recipe
            group.save()

            return render(request, 'partials/recipe_item.html', {'recipe': recipe, 'group': group})

        except Exception as e:
            # Handle any other errors that might occur
            return HttpResponse(str(e), status=400)

# ngambil pesan dari grup tertentu
def get_messages(request, group_id):
    # Cek apakah grup ada
    group = get_object_or_404(RecipeGroup, id=group_id)
    
    # Mengambil semua pesan dari grup berdasarkan ID
    messages = ChatMessage.objects.filter(group=group).order_by('timestamp')
    return render(request, 'partials/messages.html', {'messages': messages, 'user': request.user})

# Mengirim pesan baru
def send_message(request):
    if request.method == "POST":
        group_id = request.POST.get('group_id')
        content = request.POST.get('content')

        if not group_id or not content:
            return HttpResponse("Group ID or content is missing.", status=400)

        # Cek jika grup valid
        group = get_object_or_404(RecipeGroup, id=group_id)
        
        # Buat pesan baru
        message = ChatMessage.objects.create(group=group, user=request.user, message=content)

        # Mengembalikan pesan yang baru dibuat dalam konteks
        return render(request, 'partials/messages.html', {'messages': [message], 'user': request.user})

    return HttpResponse("Invalid request method.", status=405)

# hapus grup resep berdasarkan ID
def delete_group(request, group_id):
    group = get_object_or_404(RecipeGroup, id=group_id)
    
    # Pastikan grup ada sebelum dihapus
    if group.recipe:  # Memastikan grup memiliki resep yang terkait
        group.delete()
        return redirect('ask_recipe:ask_recipe')
    
    return HttpResponse("Grup tidak memiliki resep yang terkait atau grup tidak ditemukan.", status=400)

# hapus pesan berdasarkan ID
@csrf_exempt
@require_POST
def delete_message(request, message_id):
    message = get_object_or_404(ChatMessage, id=message_id)
    message.delete()
    return redirect('ask_recipe:ask_recipe')

@csrf_exempt
def search_recipe(request):
    query = request.GET.get('q', '')
    recipes = Recipe.objects.filter(title__icontains=query)
    
    if not recipes:
        return HttpResponse("No recipes found.", status=404)
    
    return render(request, 'partials/recipe_list.html', {'recipes': recipes})

# ngambil resep berdasarkan pengguna saat ini dengan xml
def show_xml(request):
    data = Recipe.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

# ngambil resep berdasarkan pengguna saat ini dengan json
def show_json(request):
    data = Recipe.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

# ngambil resep berdasarkan id dengan xml
def show_xml_by_id(request, id):
    data = Recipe.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

# ngambil resep berdasarkan id dengan json
def show_json_by_id(request, id):
    data = Recipe.objects.filter(pk=id)
    if not data:
        return HttpResponse("Recipe not found.", status=404)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json"),

@csrf_exempt
@require_POST
@login_required
def create_recipe_flutter(request):
    try:
        # Parse data JSON dari request body
        data = json.loads(request.body)
        title = data.get("title")
        ingredients = data.get("ingredients")
        instructions = data.get("instructions") 
        cooking_time = data.get("cooking_time")
        servings = data.get("servings")

        # Validasi data: pastikan semua field ada dan tidak kosong
        if not all([title, ingredients, instructions, cooking_time, servings]):
            return JsonResponse({"error": "All fields are required"}, status=400)

        # Normalisasi judul (menghapus spasi berlebih dan konversi ke lowercase)
        normalized_title = ' '.join(title.lower().split())

        # Validasi jika resep dengan nama yang sama sudah ada
        existing_recipes = Recipe.objects.all()
        for existing_recipe in existing_recipes:
            existing_normalized_title = ' '.join(existing_recipe.title.lower().split())
            if normalized_title == existing_normalized_title:
                return JsonResponse({
                    "error": f"Recipe with the name '{title}' already exists."
                }, status=400)

        # Membuat grup diskusi
        group = RecipeGroup.objects.create(
            name=f"Discussion for {title}",
            description=f"Discussion group for {title}",
            created_by=request.user
        )

        # Membuat resep baru
        recipe = Recipe.objects.create(
            group=group,
            title=title,
            ingredients=ingredients,
            instructions=instructions,
            cooking_time=cooking_time,
            servings=servings,
            added_by=request.user
        )
        recipe.save()

        return JsonResponse({
            "message": "Recipe created successfully",
            "recipe_id": str(recipe.id),
            "status":"success"
        }, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@csrf_exempt
@require_POST
@login_required
def update_recipe_flutter(request, recipe_id):
    try:
        # Pastikan recipe_id adalah UUID
        recipe = get_object_or_404(Recipe, id=recipe_id)

        # Parsing data JSON dari request body
        data = json.loads(request.body)
        title = data.get("title")
        ingredients = data.get("ingredients")
        instructions = data.get("instructions")
        cooking_time = data.get("cooking_time")
        servings = data.get("servings")

        # Validasi data
        if not all([title, ingredients, instructions, cooking_time, servings]):
            return JsonResponse({"error": "All fields are required"}, status=400)

        # Normalisasi title
        normalized_title = ' '.join(title.lower().split())

        # Update fields pada Recipe
        recipe.title = title
        recipe.ingredients = ingredients
        recipe.instructions = instructions
        recipe.cooking_time = cooking_time
        recipe.servings = servings

        # Simpan perubahan
        recipe.save()

        return JsonResponse({
            "message": "Recipe updated successfully",
            "recipe_id": str(recipe.id),
            "status": "success"
        }, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def delete_recipe(request, recipe_id):
    if request.method == 'DELETE':
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        try:
            recipe.delete()
            return JsonResponse({'message': 'Recipe deleted successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'message': f'Failed to delete recipe: {str(e)}'}, status=500)
    return JsonResponse({'message': 'Invalid HTTP method'}, status=405)