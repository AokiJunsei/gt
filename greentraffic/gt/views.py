from django.shortcuts import render,get_object_or_404,HttpResponseRedirect

##from .models import MapChange
##from .models import MapDelete
from .models import models


def top_page(request):
    return render(request, 'gt/top.html')





def admin_map_change(request, pk):
    map_change = get_object_or_404(MapChange, pk=pk)
    return render(request, 'gt/admin_map_change.html', {'map_change': map_change})



def admin_map_delete(request, pk):
    map_delete = get_object_or_404(MapDelete, pk=pk)
    return render(request, 'gt/admin_map_delete.html', {'map_delete': map_delete})



def admin_map_register(request):
    return render(request, 'gt/admin_map_register.html')



#利用者ページへ遷移する関数書く



def admin_map_detail(request, pk):
    map_object = get_object_or_404(models, pk=pk)
    return render(request, 'gt/map_detail.html', {'map_object': map_object})




def user_info(request):
    return render(request, 'user_info.html')



def user_update_view(request):
    return render(request, 'user_update.html')



def user_delete_view(request):
    return render(request, 'user_delete.html')



def account_history_view(request):
    return render(request, 'user_log.html')



def log_detail_view(request):
    return render(request, 'user_log_detail.html')



def signup_view(request):
    return render(request, 'create.html')



def login_view(request):
    return render(request, 'user_login.html')