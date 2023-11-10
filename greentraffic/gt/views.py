from django.shortcuts import render,get_object_or_404,HttpResponseRedirect

from .models import MapChange
from .models import MapDelete
from .models import models


def top_page(request):
    return render(request, 'gt/top.html')





def admin_map_change(request, pk):
    map_change = get_object_or_404(MapChange, pk=pk)
    return render(request, 'admin_map_change.html', {'map_change': map_change})



def admin_map_delete(request, pk):
    map_delete = get_object_or_404(MapDelete, pk=pk)
    return render(request, 'admin_map_delete.html', {'map_delete': map_delete})



def admin_map_register(request):
    return render(request, 'admin_map_register.html')



def map_detail(request, pk):
    map_object = get_object_or_404(models, pk=pk)
    return render(request, 'map_detail.html', {'map_object': map_object})
