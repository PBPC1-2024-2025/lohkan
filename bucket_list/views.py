from django.shortcuts import render, redirect, reverse
from bucket_list.forms import BucketListForm
from bucket_list.models import BucketList
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required


@csrf_exempt
@require_POST
def add_bucket_list(request):
    user = request.user
    name = strip_tags(request.POST.get('name'))
    
    new_bucket_list = BucketList(user=user, name=name)
    new_bucket_list.save()
    
    return HttpResponse(b"CREATED", status=201)

@login_required
def show_bucket_list(request):
    return render(request, "bucket_list.html")

def show_json(request):
    data = BucketList.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")