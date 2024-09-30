from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def show_main(request):

    context = {
        'nama': 'admin',
        'deskripsi': 'lorem ipsum',
        'harga': '20000',

    }

    return render(request, "main.html", context)
