from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .models import RecipeGroup, ChatMessage
from .forms import RecipeGroupForm, ChatMessageForm

def ask_recipe(request):
    return render(request, 'ask_recipe.html')

#untuk ngebuat grup resep baru
def create_recipe_group(request):
    if request.method == 'POST':
        form = RecipeGroupForm(request.POST)
        if form.is_valid():
            recipe_group = form.save(commit=False)
            recipe_group.created_by = request.user
            recipe_group.save()
            return redirect('group_list') 
    else:
        form = RecipeGroupForm()
    return render(request, 'create_recipe.html', {'form': form})

#untuk nampilin daftar grup
def group_list(request):
    groups = RecipeGroup.objects.all()
    return render(request, 'group_list.html', {'groups': groups})

#untuk menampilkan detail grup
def group_detail(request, id):
    group = get_object_or_404(RecipeGroup, pk=id)
    messages = ChatMessage.objects.filter(group=group).order_by('timestamp')
    return render(request, 'group_detail.html', {
        'group': group,
        'messages': messages,
        'form': ChatMessageForm()
    })

#untuk nambahin pesan baru
@csrf_exempt
def add_chat_message(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        content = request.POST.get('content')
        group = get_object_or_404(RecipeGroup, pk=id)

        # Buat pesan baru
        message = ChatMessage.objects.create(
            group=group,
            user=request.user,
            content=content
        )
        
        # Buat respons HTML
        response_content = f"<p><strong>{message.user.username}:</strong> {message.content} <em>{message.timestamp}</em></p>"
        return HttpResponse(response_content)