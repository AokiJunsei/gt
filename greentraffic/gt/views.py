from django.shortcuts import render,get_object_or_404,HttpResponseRedirect

##from .models import MapChange
##from .models import MapDelete
from .models import models


from .forms import LocationForm
from .models import Map




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





##画面遷移の関数はここより上に書きます







#form系関数



def save_location(request):
    form = LocationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            latitude = form.cleaned_data['latitude']
            longitude = form.cleaned_data['longitude']
            
            # Mapモデルにデータを保存
            map_instance = Map(
                location_name=name,
                account=request.user.account,  # 仮にユーザーアカウントがある場合
                category='gt_category',  # カテゴリを適切なものに変更
                address=address,
                coordinates={'latitude': latitude, 'longitude': longitude}
            )
            map_instance.save()

            return render(request, 'admin_map_change.html', {'form': form, 'name': name, 'address': address})
    
    return render(request, 'top.html', {'form': form})