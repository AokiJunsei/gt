from django.shortcuts import render,get_object_or_404,HttpResponseRedirect,redirect

##from .models import MapChange
##from .models import MapDelete
from .models import models


from .forms import LocationForm
from .models import Map


from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Spot
from .forms import SpotDeleteForm, MapDeleteForm

from .forms import LocationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import AccountDeleteForm

from django.contrib.auth.decorators import login_required

from .models import SearchHistory


from .forms import AccountUpdateForm
from .models import Account



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
    return render(request, 'gt/user_info.html')



def user_update_view(request):
    return render(request, 'gt/user_update.html')



def user_delete_view(request):
    return render(request, 'gt/user_delete.html')



def account_history_view(request):
    return render(request, 'gt/user_log.html')



def log_detail_view(request):
    return render(request, 'gt/user_log_detail.html')



def signup_view(request):
    return render(request, 'gt/create.html')



def login_view(request):
    return render(request, 'gt/user_login.html')





##画面遷移の関数はここより上に書きます







##########admin_map_change.htmlにおける関数##########

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




            return render(request, 'top.html', {'form': form, 'name': name, 'address': address})
    
    return render(request, 'admin_map_change.html', {'form': form})





##########admin_map_delete.htmlにおける関数##########

def delete_spot(request, spot_id):
    spot = get_object_or_404(Spot, pk=spot_id)
    if request.method == 'POST':
        form = SpotDeleteForm(request.POST, instance=spot)
        if form.is_valid():
            spot.delete()
            return HttpResponseRedirect(reverse('top.html'))
    else:
        form = SpotDeleteForm(instance=spot)
    
    return render(request, 'admin_map_delete.html', {'form': form})

def delete_map(request, map_id):
    map_instance = get_object_or_404(Map, pk=map_id)
    if request.method == 'POST':
        form = MapDeleteForm(request.POST, instance=map_instance)
        if form.is_valid():
            map_instance.delete()
            return HttpResponseRedirect(reverse('top.html'))
    else:
        form = MapDeleteForm(instance=map_instance)
    
    return render(request, 'admin_map_delete.html', {'form': form})






##########admin_map_register.htmlにおける関数##########


def save_location(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            
            return render(request, 'top.html', {'name': name, 'address': address})
    else:
        form = LocationForm()
    
    return render(request, 'admin_map_register.html', {'form': form})





##########user_delete.htmlにおける関数##########

def delete_account(request):
    if request.method == 'POST':
        form = AccountDeleteForm(request.POST)
        if form.is_valid():
            confirm_username = form.cleaned_data['confirm_username']
            user = User.objects.get(pk=request.user.id)
            if user.username == confirm_username:
                user.delete()
                logout(request)
                return redirect('top.html')
    else:
        form = AccountDeleteForm()
    
    return render(request, 'user_delete.html', {'form': form})





##########user_info.htmlにおける関数##########

@login_required
def my_page(request):
    user_info = {
        'name': request.user.account.first_name + " " + request.user.account.last_name,
        'old': 'Age Value',  # 年齢がDBのカラムにないから付け足す
        'address': request.user.account.address,
        'email': request.user.email
    }

    return render(request, 'user_info.html', {'user': user_info})





##########user_log_detail.htmlにおける関数##########

def search_history_detail(request, history_id):
    
    search_history = get_object_or_404(SearchHistory, history_id=history_id)

    context = {
        'object': search_history
    }

    return render(request, 'user_log_detail.html', context)





##########user_update.htmlにおける関数##########

def account_update(request):
    user_account = Account.objects.get(user=request.user)

    if request.method == 'POST':
        form = AccountUpdateForm(request.POST, instance=user_account)
        if form.is_valid():
            form.save()
            return redirect('top.html')
    else:
        form = AccountUpdateForm(instance=user_account)

    context = {
        'form': form
    }
    return render(request, 'user_update.html', context)