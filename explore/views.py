from django.shortcuts import render

def show_explore(request):
    context = {
        'test': 'test',
    }

    return render(request, "explore.html", context)