from django.shortcuts import render

def top_page(request):
    return render(request, 'gt/top.html')
