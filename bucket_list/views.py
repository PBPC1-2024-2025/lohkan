from django.shortcuts import render, redirect
from main.forms import BucketListForm
from main.models import BucketList
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.utils.html import strip_tags

@csrf_exempt
@require_POST
def add_bucket_list(request):
    user = request.user
    name = strip_tags(request.POST.get('name'))
    
    new_bucket_list = BucketList(user=user, name=name)
    new_bucket_list.save()
    
    return HttpResponse(b"CREATED", status=201)