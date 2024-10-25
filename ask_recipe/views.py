from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import RecipeGroup, ChatMessage, Recipe
from .forms import RecipeGroupForm, ChatMessageForm
from django.http import HttpResponse
from django.core import serializers

def ask_recipe(request):
    recipes = Recipe.objects.all()  # Ambil semua resep dari database
    return render(request, 'ask_recipe.html', {'recipes': recipes})

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

        # Pastikan semua data valid sebelum disimpan
        if not title or not ingredients or not instructions or not cooking_time or not servings:
            return HttpResponse("Incomplete data", status=400)
        
        # Buat grup otomatis untuk diskusi resep ini
        group = RecipeGroup.objects.create(
            name=f"Discussion for {title}",
            description=f"Discussion group for {title}",
            created_by=request.user
        )

        # Buat resep dan hubungkan dengan grup
        recipe = Recipe.objects.create(
            group=group,
            title=title,
            ingredients=ingredients,
            instructions=instructions,
            cooking_time=int(cooking_time), 
            servings=int(servings),
            added_by=request.user
        )

        return render(request, 'partials/recipe_item.html', {'recipe': recipe})

# Mengambil pesan dari grup tertentu
def get_messages(request, group_id):
    messages = ChatMessage.objects.filter(group_id=group_id).order_by('timestamp')
    return render(request, 'partials/messages.html', {'messages': messages, 'user': request.user})

# Mengirim pesan baru
def send_message(request):
    if request.method == "POST":
        group_id = request.POST.get('group_id')
        content = request.POST.get('content')

        if not group_id or not content:
            return HttpResponse("Group ID or content is missing.", status=400)

        group = get_object_or_404(RecipeGroup, id=group_id)
        message = ChatMessage.objects.create(group=group, user=request.user, message=content)

        return HttpResponse(
             f"""
            <div class="flex justify-end mb-4">
                <div class="bg-red-800 text-white p-4 rounded-xl shadow-md max-w-md">
                    <p class="text-xs font-semibold mb-1 text-gray-300">{message.user.username}</p>
                    <p class="text-sm leading-relaxed break-words">{message.message}</p>
                    <p class="text-xs text-gray-300 mt-2">
                        {message.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
                    </p>
                </div>
            </div>
            """, content_type="text/html"
        )

    return HttpResponse("Invalid request method.", status=405)

def delete_group(request, group_id):
    group = get_object_or_404(RecipeGroup, id=group_id)
    group.delete()
    return redirect('ask_recipe:ask_recipe')

@csrf_exempt
@require_POST
def delete_message(request, message_id):
    message = get_object_or_404(ChatMessage, id=message_id)
    message.delete()
    return redirect('ask_recipe:ask_recipe')

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
