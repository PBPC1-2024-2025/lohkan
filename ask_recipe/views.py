import uuid
import json
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import RecipeGroup, ChatMessage, Recipe
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from .forms import RecipeForm

def ask_recipe(request):
    # Mengambil semua resep dari database
    recipes = Recipe.objects.all()
    return render(request, 'ask_recipe.html', {'recipes': recipes})

# Membuat grup resep baru di web django
@csrf_exempt
@require_POST
def create_recipe(request):
    if request.method == "POST":
        try:
            # Mengambil data dari request POST
            title = request.POST.get("title")
            ingredients = request.POST.get("ingredients")
            instructions = request.POST.get("instructions")
            cooking_time = int(request.POST.get("cooking_time"))
            servings = int(request.POST.get("servings"))
            image = request.FILES.get("image")  # Mengambil gambar dari formulir

            # Validasi data yang dibutuhkan
            if not title or not ingredients or not instructions or not cooking_time or not servings or not image:
                return HttpResponse("Semua kolom wajib diisi, termasuk gambar.", status=400)

            # Menormalkan judul (menghapus spasi ekstra dan mengubah menjadi huruf kecil)
            normalized_title = ' '.join(title.lower().split())

            # Memeriksa apakah sudah ada resep dengan nama yang sama
            existing_recipes = Recipe.objects.all()
            for existing_recipe in existing_recipes:
                existing_normalized_title = ' '.join(existing_recipe.title.lower().split())
                if normalized_title == existing_normalized_title:
                    return HttpResponse(
                        f"Resep dengan nama '{title}' sudah ada.", 
                        status=400
                    )

            # Membuat grup terlebih dahulu
            group_name = f"Diskusi untuk {title}"
            group = RecipeGroup.objects.create(
                name=group_name,
                description=f"Grup diskusi untuk {title}",
            )

            # Menyimpan gambar
            filename = f"recipe_images/{uuid.uuid4()}_{image.name}"
            image_path = default_storage.save(filename, ContentFile(image.read()))

            # Membuat resep dengan referensi grup
            recipe = Recipe.objects.create(
                title=title,
                ingredients=ingredients,
                instructions=instructions,
                cooking_time=cooking_time, 
                servings=servings,
                added_by=User.objects.get(username='admin'),
                group=group,
                image=image_path  # Menyimpan path gambar ke model
            )

            # Memperbarui grup dengan referensi resep jika diperlukan
            group.recipe = recipe
            group.save()

            return render(request, 'partials/recipe_item.html', {'recipe': recipe, 'group': group})

        except Exception as e:
            # Menangani kesalahan lain yang mungkin terjadi
            return HttpResponse(str(e), status=400)

# Mengedit resep di web django
@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)  # Mengambil resep berdasarkan UUID

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)  # Menambahkan request.FILES
        if form.is_valid():
            # Menangani upload gambar
            if 'image' in request.FILES:
                image = request.FILES['image']
                filename = f"recipe_images/{uuid.uuid4()}_{image.name}"
                image_path = default_storage.save(filename, ContentFile(image.read()))
                recipe.image = image_path  # Memperbarui path gambar di model

            # Memeriksa apakah ada resep lain dengan judul yang sama
            title = form.cleaned_data.get("title")
            normalized_title = ' '.join(title.lower().split())  # Menormalkan judul

            # Memeriksa jika ada resep lain dengan judul yang sama
            existing_recipes = Recipe.objects.exclude(id=recipe.id)  # Mengecualikan resep yang sedang diedit
            for existing_recipe in existing_recipes:
                existing_normalized_title = ' '.join(existing_recipe.title.lower().split())
                if normalized_title == existing_normalized_title:
                    form.add_error('title', f"Resep dengan nama '{title}' sudah ada.")  # Menambahkan error ke field 'title'
                    break

            if form.errors:
                return render(request, 'partials/edit_recipe.html', {'form': form, 'recipe': recipe})  # Jika ada error, tampilkan form lagi

            form.save()  # Menyimpan perubahan
            return redirect('ask_recipe:ask_recipe')  # Mengarahkan ke halaman utama setelah edit
    else:
        form = RecipeForm(instance=recipe)

    return render(request, 'partials/edit_recipe.html', {'form': form, 'recipe': recipe})

# Mengambil pesan dari grup tertentu di web django
def get_messages(request, group_id):
    # Memeriksa apakah grup ada
    group = get_object_or_404(RecipeGroup, id=group_id)
    
    # Mengambil semua pesan dari grup berdasarkan ID
    messages = ChatMessage.objects.filter(group=group).order_by('timestamp')
    return render(request, 'partials/messages.html', {'messages': messages, 'user': request.user})

# Mengirim pesan baru di web django
def send_message(request):
    if request.method == "POST":
        group_id = request.POST.get('group_id')
        content = request.POST.get('content')

        if not group_id or not content:
            return HttpResponse("Group ID atau konten tidak ada.", status=400)

        # Memeriksa apakah grup valid
        group = get_object_or_404(RecipeGroup, id=group_id)
        
        # Membuat pesan baru
        message = ChatMessage.objects.create(group=group, user=request.user, message=content)

        # Mengembalikan pesan yang baru dibuat dalam konteks
        return render(request, 'partials/messages.html', {'messages': [message], 'user': request.user})

    return HttpResponse("Metode request tidak valid.", status=405)

# Menghapus grup resep berdasarkan ID di web django
def delete_group(request, group_id):
    group = get_object_or_404(RecipeGroup, id=group_id)
    
    # Memastikan grup memiliki resep yang terkait sebelum dihapus
    if group.recipe:  
        group.delete()
        return redirect('ask_recipe:ask_recipe')
    
    return HttpResponse("Grup tidak memiliki resep yang terkait atau grup tidak ditemukan.", status=400)

# Menghapus pesan berdasarkan ID di web django
@csrf_exempt
@require_POST
def delete_message(request, message_id):
    message = get_object_or_404(ChatMessage, id=message_id)
    message.delete()
    return redirect('ask_recipe:ask_recipe')

# Mencari nama resep di web django
@csrf_exempt
def search_recipe(request):
    query = request.GET.get('q', '')
    recipes = Recipe.objects.filter(title__icontains=query)
    
    if not recipes:
        return HttpResponse("Resep tidak ditemukan.", status=404)
    
    return render(request, 'partials/recipe_list.html', {'recipes': recipes})

# Mengambil resep berdasarkan pengguna saat ini dalam format XML
def show_xml(request):
    data = Recipe.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

# Mengambil resep berdasarkan pengguna saat ini dalam format JSON
def show_json(request):
    recipes = Recipe.objects.all()
    recipe_data = []

    for recipe in recipes:
        # Serialisasi resep
        recipe_serialized = serializers.serialize("json", [recipe])
        recipe_json = json.loads(recipe_serialized)[0]  # Mengambil resep pertama

        # Menambahkan URL absolut untuk gambar
        if recipe.image:
            recipe_json['fields']['image_url'] = request.build_absolute_uri(recipe.image.url)
        else:
            recipe_json['fields']['image_url'] = None

        recipe_data.append(recipe_json)

    return HttpResponse(json.dumps(recipe_data), content_type="application/json")

# Mengambil resep berdasarkan ID dalam format XML
def show_xml_by_id(request, id):
    data = Recipe.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

# Mengambil resep berdasarkan ID dalam format JSON
def show_json_by_id(request, id):
    data = Recipe.objects.filter(pk=id)
    if not data:
        return HttpResponse("Resep tidak ditemukan.", status=404)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

# Membuat grup resep baru di flutter app
@csrf_exempt
@require_POST
def create_recipe_flutter(request):
    try:
        # Mengambil data dari request
        title = request.POST.get('title')
        ingredients = request.POST.get('ingredients')
        instructions = request.POST.get('instructions')
        cooking_time = int(request.POST.get('cooking_time'))
        servings = int(request.POST.get('servings'))
        image = request.FILES.get('image')  # Mengambil gambar jika ada

        # Validasi data
        if not all([title, ingredients, instructions, cooking_time, servings, image]):
            return JsonResponse({'status': 'error', 'message': 'Semua kolom wajib diisi'}, status=400)

        # Menormalkan judul
        normalized_title = ' '.join(title.lower().split())

        # Memeriksa resep yang sudah ada
        existing_recipes = Recipe.objects.all()
        for existing_recipe in existing_recipes:
            existing_normalized_title = ' '.join(existing_recipe.title.lower().split())
            if normalized_title == existing_normalized_title:
                return JsonResponse(
                    {'status': 'error', 'message': f"Resep dengan nama '{title}' sudah ada."},
                    status=400
                )

        # Menyimpan gambar
        if image:
            filename = f"recipe_images/{uuid.uuid4()}_{image.name}"
            image_path = default_storage.save(filename, ContentFile(image.read()))
        else:
            image_path = None

        # Membuat grup resep
        group = RecipeGroup.objects.create(
            name=title,
            description=f"Diskusi untuk Resep {title}",
        )

        # Membuat resep
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
            'message': 'Resep berhasil dibuat',
            'recipe_id': str(recipe.id),
        }, status=201)

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Terjadi kesalahan: {str(e)}'}, status=500)

# Mengedit resep di web django di flutter app
@csrf_exempt
@require_POST
def update_recipe_flutter(request, recipe_id):
    try:
        # Memastikan recipe_id adalah UUID
        recipe = get_object_or_404(Recipe, id=recipe_id)

        # Mengambil data dari request
        title = request.POST.get('title')
        ingredients = request.POST.get('ingredients')
        instructions = request.POST.get('instructions')
        cooking_time = int(request.POST.get('cooking_time'))
        servings = int(request.POST.get('servings'))
        image = request.FILES.get('image')  # Mengambil gambar jika ada

        # Validasi data
        if not all([title, ingredients, instructions, cooking_time, servings]):
            return JsonResponse({'status': 'error', 'message': 'Semua kolom wajib diisi'}, status=400)

        # Validasi angka (waktu memasak dan porsi)
        if cooking_time <= 0 or servings <= 0:
            return JsonResponse({'status': 'error', 'message': 'Waktu memasak dan porsi harus lebih besar dari 0'}, status=400)

        # Menyimpan gambar jika ada
        if image:
            filename = f"recipe_images/{uuid.uuid4()}_{image.name}"
            image_path = default_storage.save(filename, ContentFile(image.read()))
            recipe.image = image_path  # Memperbarui path gambar di model

        # Memperbarui fields pada Recipe
        recipe.title = title
        recipe.ingredients = ingredients
        recipe.instructions = instructions
        recipe.cooking_time = cooking_time
        recipe.servings = servings

        # Menyimpan perubahan
        recipe.save()

        return JsonResponse({
            'status': 'success',
            'message': 'Resep berhasil diperbarui',
            'recipe_id': str(recipe.id),
        }, status=200)

    except ValueError:
        return JsonResponse({'status': 'error', 'message': 'Waktu memasak dan porsi harus berupa angka yang valid'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Terjadi kesalahan: {str(e)}'}, status=500)

# Menghapus resep berdasarkan ID di flutter app
@csrf_exempt
def delete_recipe(request, recipe_id):
    if request.method == 'DELETE':  # Menangani permintaan POST
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        try:
            recipe.delete()
            return JsonResponse({'message': 'Resep berhasil dihapus'}, status=200)
        except Exception as e:
            return JsonResponse({'message': f'Gagal menghapus resep: {str(e)}'}, status=500)
    return JsonResponse({'message': 'Metode HTTP tidak valid'}, status=405)

# Mengambil pesan dari grup tertentu di flutter app
@csrf_exempt
def get_chat_messages(request):
    if request.method == 'GET':
        group_id = request.GET.get('group_id')  # Mengambil group_id dari query string
        if not group_id:
            return JsonResponse({'error': 'group_id diperlukan'}, status=400)

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
            return JsonResponse({'error': 'Grup tidak ditemukan'}, status=404)

# Mengirim pesan baru di flutter app       
@csrf_exempt
def send_chat_message(request):
    try:
        # Parse JSON data dari body request
        data = json.loads(request.body)
        
        group_id = data.get('group_id')
        message_text = data.get('message')

        if not group_id or not message_text:
            return JsonResponse({'error': 'group_id dan message diperlukan'}, status=400)

        try:
            group = RecipeGroup.objects.get(id=group_id)
    
            # Membuat pesan baru
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
            return JsonResponse({'error': 'Grup tidak ditemukan'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    except json.JSONDecodeError as e:
        return JsonResponse({'error': 'Data JSON tidak valid'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Menghapus pesan berdasarkan ID di flutter app
@csrf_exempt
def delete_chat_message(request, message_id):
    if request.method == 'DELETE':
        message = get_object_or_404(ChatMessage, id=message_id)
        try:
            message.delete()
            return JsonResponse({'message': 'Pesan berhasil dihapus'}, status=200)
        except Exception as e:
            return JsonResponse({'message': f'Gagal menghapus pesan: {str(e)}'}, status=500)
    return JsonResponse({'message': 'Metode HTTP tidak valid'}, status=405)
