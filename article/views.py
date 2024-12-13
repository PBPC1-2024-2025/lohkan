from django.shortcuts import render, redirect, reverse , get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from article.models import Article, Comment
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.core import serializers
from django.contrib import messages
from django.core.paginator import Paginator
import uuid
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required

# menampilkan semua artikel
def full_article(request):
    article_list = Article.objects.all().order_by('-id')
    return render(request, 'full_article.html', {'article_list': article_list})

# # membuat artikel baru
# @csrf_exempt
# @require_POST
# def create_article(request):
#    title = request.POST.get("title")
#    description = request.POST.get("description")
#    image = request.FILES.get('image') 

#    new_article = Article(
#       title=title, description=description, image=image
#    )
#    new_article.save()

#    return HttpResponse(b"CREATED", status=201)

from django.http import JsonResponse  # Gunakan JsonResponse untuk respons JSON
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

@csrf_exempt
@require_POST
def create_article(request):
    try:
        title = request.POST.get("title", "")
        description = request.POST.get("description", "")
        image = request.FILES.get('image')

        # Validasi input
        if not title or not description:
            return JsonResponse({
                'status': 'error', 
                'message': 'Title and description are required'
            }, status=400)

        new_article = Article(
            title=title, 
            description=description, 
            image=image
        )
        new_article.save()

        return JsonResponse({
            'status': 'success', 
            'message': 'Article created successfully',
            'article_id': new_article.id
        }, status=201)

    except Exception as e:
        return JsonResponse({
            'status': 'error', 
            'message': str(e)
        }, status=500)

@csrf_exempt
@require_POST
def create_article_flutter(request):
    try:
        # Ambil data dari request
        title = request.POST.get("title", "")
        description = request.POST.get("description", "")
        image = request.FILES.get('image')

        # Validasi input
        if not title or not description:
            return JsonResponse({
                'status': 'error', 
                'message': 'Title and description are required'
            }, status=400)

        # Simpan gambar jika ada
        image_path = None
        if image:
            # Buat path penyimpanan unik
            file_extension = os.path.splitext(image.name)[1]
            filename = f"articles/{uuid.uuid4()}{file_extension}"
            
            # Simpan file
            path = default_storage.save(filename, ContentFile(image.read()))
            image_path = path

        # Buat artikel baru
        new_article = Article(
            title=title, 
            description=description, 
            image=image_path  # Simpan path gambar
        )
        new_article.save()

        return JsonResponse({
            'status': 'success', 
            'message': 'Article created successfully',
            'article_id': new_article.id
        }, status=201)

    except Exception as e:
        return JsonResponse({
            'status': 'error', 
            'message': str(e)
        }, status=500)

# @csrf_exempt
# # menghapus artikel
# def delete_article(request, id):
#     if request.method == 'DELETE':
#         article = Article.objects.get(pk = id)
#         article.delete()
#         return HttpResponse

@csrf_exempt
def delete_article(request, id):
    if request.method == 'DELETE':
        try:
            # Coba ambil artikel berdasarkan ID
            article = Article.objects.filter(pk=id).first()
            if not article:
                return JsonResponse({'error': 'Article not found.'}, status=404)
            # Hapus artikel jika ditemukan
            article.delete()
            return HttpResponse(status=204)  # 204 No Content jika sukses
        except Exception as e:
            # Log error untuk debugging
            print(f"Error deleting article: {e}")
            return JsonResponse({'error': 'An error occurred while deleting the article.'}, status=500)
    else:
        article = Article.objects.get(pk=id)
        article.delete()
        return HttpResponseRedirect(reverse('article:full_article'))
    return JsonResponse({'error': 'Invalid HTTP method.'}, status=405)


@csrf_exempt
# mengedit artikel
def edit_article(request, id):
    article = Article.objects.filter(pk=id).first() 
    if not article:
        messages.error(request, 'Article not found.')
        return redirect('article:full_article')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')  

        if not title or not description:
            messages.error(request, 'Please fill in all fields first.')

        else:
            article.title = title
            article.description = description
            
            if image:
                article.image = image

            article.save()
            messages.success(request, 'Article successfully updated.')
            return redirect('article:full_article')
        
    context = {
        'article':  article
    }
    return render(request, 'edit_article.html', context)

# menampilkan detail artikel
def article_detail(request, id):
    article = get_object_or_404(Article, pk=id)
    comments = Comment.objects.filter(article=article).order_by('-created_at') 
    return render(request, 'article.html', {'article': article, 'comments': comments})

@csrf_exempt
def add_comment(request, id):  
    article = get_object_or_404(Article, pk=id) 
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(article=article, content=content, user=request.user)
            return redirect('article:article_detail', id=id)  
    return redirect('article:article_detail', id=id)

@csrf_exempt  
def add_comment_flutter(request, id):
    article = get_object_or_404(Article, pk=id)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            content = data.get('content')
            
            if content:
                # Create a new comment
                Comment.objects.create(article=article, content=content, user=request.user)
                return JsonResponse({'message': 'Comment added successfully'}, status=201)
            else:
                return JsonResponse({'error': 'Content is required'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)



# menampilkan artikel dalam format JSON
def show_xml(request):
   data = Article.objects.all()
   return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

# menampilkan artikel berdasarkan id dalam format JSON
def show_json(request):
    articles = Article.objects.all()
    article_data = []

    for article in articles:
        # Ambil komentar terkait artikel
        comments = Comment.objects.filter(article=article)
        comment_list = []

        for comment in comments:
            comment_list.append({
                'id': comment.id,
                'user': comment.user.username,  # Asumsikan ada relasi dengan User
                'content': comment.content,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),  # Konversi datetime ke string
            })

        # Serialisasi artikel
        article_serialized = serializers.serialize("json", [article])
        article_json = json.loads(article_serialized)[0]  # Ambil artikel pertama

        # Tambahkan URL absolut untuk gambar
        if article.image:
            article_json['fields']['image'] = request.build_absolute_uri(article.image.url)
        else:
            article_json['fields']['image'] = None

        # Tambahkan komentar ke dalam data artikel
        article_json['fields']['comments'] = comment_list
        article_data.append(article_json)

    return HttpResponse(json.dumps(article_data), content_type="application/json")

# menampilkan artikel berdasarkan id dalam format JSON
def show_xml_by_id(request, id):
    data = Article.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

# menampilkan artikel berdasarkan id dalam format JSON
def show_json_by_id(request, id):
    try:
        article = Article.objects.get(pk=id)
        comments = Comment.objects.filter(article=article)
        comment_list = []

        for comment in comments:
            comment_list.append({
                'id': comment.id,
                'user': comment.user.username,  # Asumsikan ada relasi dengan User
                'content': comment.content,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),  # Konversi datetime ke string
            })

        # Serialisasi artikel
        article_serialized = serializers.serialize("json", [article])
        article_json = json.loads(article_serialized)[0]  # Ambil artikel pertama

        # Tambahkan URL absolut untuk gambar
        if article.image:
            article_json['fields']['image'] = request.build_absolute_uri(article.image.url)
        else:
            article_json['fields']['image'] = None

        # Tambahkan komentar ke dalam data artikel
        article_json['fields']['comments'] = comment_list

        return HttpResponse(json.dumps(article_json), content_type="application/json")
    
    except Article.DoesNotExist:
        return HttpResponse(
            json.dumps({'error': 'Article not found'}), 
            content_type="application/json", 
            status=404
        )
def index(request):
    return render(request, 'full_article.html')