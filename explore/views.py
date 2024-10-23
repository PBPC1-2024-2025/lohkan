from django.shortcuts import render

def show_main(request):
    context = {
        'test': 'test',
    }

    return render(request, "explore.html", context)