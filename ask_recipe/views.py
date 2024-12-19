import uuid
import json
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import RecipeGroup, ChatMessage, Recipe
from .forms import RecipeForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core import serializers

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
            )

            # Then create recipe with the group reference
            recipe = Recipe.objects.create(
                title=title,
                ingredients=ingredients,
                instructions=instructions,
                cooking_time=cooking_time, 
                servings=servings,
                added_by=User.objects.get(username='admin'),
                group=group
            )

            # Update the group with the recipe reference if needed
            group.recipe = recipe
            group.save()

            return render(request, 'partials/recipe_item.html', {'recipe': recipe, 'group': group})

        except Exception as e:
            # Handle any other errors that might occur
            return HttpResponse(str(e), status=400)

@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)  # Ambil resep berdasarkan UUID

    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('ask_recipe:ask_recipe')  # Redirect ke halaman utama setelah edit
    else:
        form = RecipeForm(instance=recipe)

    return render(request, 'partials/edit_recipe.html', {'form': form, 'recipe': recipe})

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
    recipes = Recipe.objects.all()
    recipe_data = []

    for recipe in recipes:
        # Serialisasi resep
        recipe_serialized = serializers.serialize("json", [recipe])
        recipe_json = json.loads(recipe_serialized)[0]  # Ambil resep pertama

        # Tambahkan URL absolut untuk gambar
        if recipe.image:
            recipe_json['fields']['image_url'] = request.build_absolute_uri(recipe.image.url)
        else:
            recipe_json['fields']['image_url'] = None

        recipe_data.append(recipe_json)

    return HttpResponse(json.dumps(recipe_data), content_type="application/json")

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
def create_recipe_flutter(request):
    try:
        # Ambil data dari request
        title = request.POST.get('title')
        ingredients = request.POST.get('ingredients')
        instructions = request.POST.get('instructions')
        cooking_time = int(request.POST.get('cooking_time'))
        servings = int(request.POST.get('servings'))
        image = request.FILES.get('image')  # Ambil gambar jika ada

        # Validasi data
        if not all([title, ingredients, instructions, cooking_time, servings, image]):
            return JsonResponse({'status': 'error', 'message': 'All fields are required'}, status=400)

        # Normalize the title (remove extra spaces and convert to lowercase)
        normalized_title = ' '.join(title.lower().split())

        # Check for existing recipes with normalized names
        existing_recipes = Recipe.objects.all()
        for existing_recipe in existing_recipes:
            existing_normalized_title = ' '.join(existing_recipe.title.lower().split())
            if normalized_title == existing_normalized_title:
                return JsonResponse(
                    {'status': 'error', 'message': f"Recipe with the name '{title}' already exists."},
                    status=400
                )

        # Simpan gambar
        if image:
            filename = f"recipe_images/{uuid.uuid4()}_{image.name}"
            image_path = default_storage.save(filename, ContentFile(image.read()))
        else:
            image_path = None

        # Buat grup resep
        group = RecipeGroup.objects.create(
            name=title,
            description=f"Discussion for Recipe {title}",
        )

        # Buat resep
        recipe = Recipe.objects.create(
            title=title,
            ingredients=ingredients,
            instructions=instructions,
            cooking_time=cooking_time,
            servings=servings,
            added_by=User.objects.get(username='admin'),
            group=group,
            image=image_path
        )

        return JsonResponse({
            'status': 'success',
            'message': 'Recipe created successfully',
            'recipe_id': str(recipe.id),
        }, status=201)

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Terjadi kesalahan: {str(e)}'}, status=500)
    
@csrf_exempt
@require_POST
def update_recipe_flutter(request, recipe_id):
    try:
        # Pastikan recipe_id adalah UUID
        recipe = get_object_or_404(Recipe, id=recipe_id)

        # Ambil data dari request
        title = request.POST.get('title')
        ingredients = request.POST.get('ingredients')
        instructions = request.POST.get('instructions')
        cooking_time = int(request.POST.get('cooking_time'))
        servings = int(request.POST.get('servings'))
        image = request.FILES.get('image')  # Ambil gambar jika ada

        # Validasi data
        if not all([title, ingredients, instructions, cooking_time, servings]):
            return JsonResponse({'status': 'error', 'message': 'All fields are required'}, status=400)

        # Validasi angka (cooking time dan servings)
        if cooking_time <= 0 or servings <= 0:
            return JsonResponse({'status': 'error', 'message': 'Cooking time and servings must be greater than 0'}, status=400)

        # Simpan gambar jika ada
        if image:
            filename = f"recipe_images/{uuid.uuid4()}_{image.name}"
            image_path = default_storage.save(filename, ContentFile(image.read()))
            recipe.image = image_path  # Update path gambar di model

        # Update fields pada Recipe
        recipe.title = title
        recipe.ingredients = ingredients
        recipe.instructions = instructions
        recipe.cooking_time = cooking_time
        recipe.servings = servings

        # Simpan perubahan
        recipe.save()

        return JsonResponse({
            'status': 'success',
            'message': 'Recipe updated successfully',
            'recipe_id': str(recipe.id),
        }, status=200)

    except ValueError:
        return JsonResponse({'status': 'error', 'message': 'Cooking time and servings must be valid numbers'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Terjadi kesalahan: {str(e)}'}, status=500)

@csrf_exempt
def delete_recipe(request, recipe_id):
    if request.method == 'DELETE':  # Handle POST requests
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        try:
            recipe.delete()
            return JsonResponse({'message': 'Recipe deleted successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'message': f'Failed to delete recipe: {str(e)}'}, status=500)
    return JsonResponse({'message': 'Invalid HTTP method'}, status=405)

@csrf_exempt
def get_chat_messages(request):
    if request.method == 'GET':
        group_id = request.GET.get('group_id')  # Ambil group_id dari query string
        if not group_id:
            return JsonResponse({'error': 'group_id is required'}, status=400)

        try:
            group = RecipeGroup.objects.get(id=group_id)
            messages = ChatMessage.objects.filter(group=group).order_by('timestamp')
            message_list = [
                {
                    'id': str(msg.id),
                    'user': msg.user.username,
                    'message': msg.message,
                    'timestamp': msg.timestamp.isoformat(),
                }
                for msg in messages
            ]
            return JsonResponse({'messages': message_list}, status=200)
        except RecipeGroup.DoesNotExist:
            return JsonResponse({'error': 'Group not found'}, status=404)
        
@csrf_exempt
def send_chat_message(request):
    print("Received request body:", request.body)  # Debug print
    try:
        # Parse JSON data dari body request
        data = json.loads(request.body)
        print("Parsed data:", data)  # Debug print
        print("Current user:", request.user)  # Debug print
        
        group_id = data.get('group_id')
        message_text = data.get('message')

        print(f"group_id: {group_id}, message: {message_text}")  # Debug print

        if not group_id or not message_text:
            return JsonResponse({'error': 'group_id and message are required'}, status=400)

        try:
            group = RecipeGroup.objects.get(id=group_id)
            print("Found group:", group)  # Debug print

            # Buat pesan baru
            new_message = ChatMessage.objects.create(
                group=group,
                user=request.user,
                message=message_text
            )

            return JsonResponse({
                'status': 'success',
                'id': str(new_message.id),
                'user': new_message.user.username,
                'message': new_message.message,
                'timestamp': new_message.timestamp.isoformat(),
            }, status=201)

        except RecipeGroup.DoesNotExist:
            print("Group not found!")  # Debug print
            return JsonResponse({'error': 'Group not found'}, status=404)
        except Exception as e:
            print("Error creating message:", str(e))  # Debug print
            return JsonResponse({'error': str(e)}, status=500)

    except json.JSONDecodeError as e:
        print("JSON decode error:", str(e))  # Debug print
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        print("Unexpected error:", str(e))  # Debug print
        return JsonResponse({'error': str(e)}, status=500)
    
@csrf_exempt
def delete_chat_message(request, message_id):
    if request.method == 'DELETE':
        message = get_object_or_404(ChatMessage, id=message_id)
        try:
            message.delete()
            return JsonResponse({'message': 'Message deleted successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'message': f'Failed to delete message: {str(e)}'}, status=500)
    return JsonResponse({'message': 'Invalid HTTP method'}, status=405)