from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import RecipeGroup, ChatMessage, Recipe
from .forms import RecipeGroupForm, ChatMessageForm
from django.http import HttpResponse
from django.core import serializers

def ask_recipe(request):
    return render(request, 'ask_recipe.html')

#untuk ngebuat grup resep baru
@csrf_exempt
@require_POST
def create_recipe(request):
    title = request.POST.get("title")
    ingredients = request.POST.get("ingredients")
    instructions = request.POST.get("instructions")
    cooking_time = request.POST.get("cooking_time")
    servings = request.POST.get("servings")

    new_recipe = Recipe(
        title=title, 
        ingredients=ingredients, 
        instructions=instructions,
        cooking_time=cooking_time,
        servings=servings
    )
    new_recipe.save()

    return HttpResponse(b"CREATED", status=201)

# # #untuk nampilin daftar grup
# def group_list(request):
#     groups = RecipeGroup.objects.all()
#     return render(request, 'group_list.html', {'groups': groups})

# # #untuk menampilkan detail grup
# def group_detail(request, id):
#     group = get_object_or_404(RecipeGroup, pk=id)
#     messages = ChatMessage.objects.filter(group=group).order_by('timestamp')
#     return render(request, 'group_detail.html', {
#         'group': group,
#         'messages': messages,
#         'form': ChatMessageForm()
#     })

# # #untuk nambahin pesan baru
# @csrf_exempt
# def add_chat_message(request):
#     if request.method == 'POST':
#         id = request.POST.get('id')
#         content = request.POST.get('content')
#         group = get_object_or_404(RecipeGroup, pk=id)

#         # Buat pesan baru
#         message = ChatMessage.objects.create(
#             group=group,
#             user=request.user,
#             content=content
#         )
        
#         # Buat respons HTML
#         response_content = f"<p><strong>{message.user.username}:</strong> {message.content} <em>{message.timestamp}</em></p>"
#         return HttpResponse(response_content)
    
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
