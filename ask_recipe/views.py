from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import RecipeGroup, ChatMessage, Recipe
from .forms import RecipeGroupForm, ChatMessageForm
from django.http import HttpResponse
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
        # ngambil data dari permintaan post
        title = request.POST.get("title")
        ingredients = request.POST.get("ingredients")
        instructions = request.POST.get("instructions")
        cooking_time = int(request.POST.get("cooking_time"))
        servings = int(request.POST.get("servings"))

        # mastiin semua data valid sebelum disimpan
        if not title or not ingredients or not instructions or not cooking_time or not servings:
            return HttpResponse("Incomplete data", status=400)
        
        # buat grup otomatis untuk diskusi resep ini
        group = RecipeGroup.objects.create(
            name=f"Discussion for {title}",
            description=f"Discussion group for {title}",
            created_by=request.user
        )

        # buat resep dan hubungkan dengan grup
        recipe = Recipe.objects.create(
            group=group,
            title=title,
            ingredients=ingredients,
            instructions=instructions,
            cooking_time=int(cooking_time), 
            servings=int(servings),
            added_by=request.user
        )

        # ngembaliin template dengan item resep yang baru dibua
        return render(request, 'partials/recipe_item.html', {'recipe': recipe})

# ngambil pesan dari grup tertentu
def get_messages(request, group_id):
     # ngambil semua pesan dari grup berdasarkan ID
    messages = ChatMessage.objects.filter(group_id=group_id).order_by('timestamp')
    return render(request, 'partials/messages.html', {'messages': messages, 'user': request.user})

# Mengirim pesan baru
def send_message(request):
    # ngambil data dari permintaan post
    if request.method == "POST":
        group_id = request.POST.get('group_id')
        content = request.POST.get('content')

        if not group_id or not content:
            return HttpResponse("Group ID or content is missing.", status=400)

        group = get_object_or_404(RecipeGroup, id=group_id)
        # buat pesan baru
        message = ChatMessage.objects.create(group=group, user=request.user, message=content)

        # ngembaliin pesan yang baru dibuat dalam konteks
        return render(request, 'partials/messages.html', {'messages': [message], 'user': request.user})
    
    # menangani permintaan yang tidak valid
    return HttpResponse("Invalid request method.", status=405)

# hapus grup resep berdasarkan ID
def delete_group(request, group_id):
    group = get_object_or_404(RecipeGroup, id=group_id)
    group.delete()
    return redirect('ask_recipe:ask_recipe')

# hapus pesan berdasarkan ID
@csrf_exempt
@require_POST
def delete_message(request, message_id):
    message = get_object_or_404(ChatMessage, id=message_id)
    message.delete()
    return redirect('ask_recipe:ask_recipe')

@csrf_exempt
def search_recipe(request):
    # get query pencarian dari permintaan
    query = request.GET.get('q', '')
    # filter resep berdasarkan judul (tidak case-sensitive)
    recipes = Recipe.objects.filter(title__icontains=query)
    # ngembaliin daftar resep
    return render(request, 'partials/recipe_list.html', {'recipes': recipes})

# ngambil resep berdasarkan pengguna saat ini dengan xml
def show_xml(request):
    data = Recipe.objects.filter(added_by=request.user)  # Ubah user menjadi added_by
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

# ngambil resep berdasarkan pengguna saat ini dengan json
def show_json(request):
    data = Recipe.objects.filter(added_by=request.user)  # Ubah user menjadi added_by
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

# ngambil resep berdasarkan id dengan xml
def show_xml_by_id(request, id):
    data = Recipe.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

# ngambil resep berdasarkan id dengan json
def show_json_by_id(request, id):
    data = Recipe.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
