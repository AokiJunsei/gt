from django.shortcuts import render,get_object_or_404,HttpResponseRedirect,redirect

from .models import models

from django.views.generic import TemplateView
from .forms import AccountForm, AddAccountForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Account, Map
from .forms import AccountForm, AddAccountForm, AccountDeleteForm, AccountUpdateForm, LocationForm

import logging

# ロガーの設定
logger = logging.getLogger(__name__)

# トップページのビュー
def top_page(request):
    return render(request, 'gt/top.html')

# 管理者用トップページのビュー
@login_required
def admin_top(request):
    return render(request, 'gt/admin_top.html')

# 管理者用マップ変更ビュー
@login_required
def admin_map_change(request, pk):
    map_change = get_object_or_404(Map, pk=pk)
    return render(request, 'gt/admin_map_change.html', {'map_change': map_change})

# 管理者用マップ削除ビュー
@login_required
def admin_map_delete(request, pk):
    map_delete = get_object_or_404(Map, pk=pk)
    return render(request, 'gt/admin_map_delete.html', {'map_delete': map_delete})

# 管理者用マップ詳細ビュー
@login_required
def admin_map_detail(request, pk):
    map_object = get_object_or_404(Map, pk=pk)
    return render(request, 'gt/map_detail.html', {'map_object': map_object})

# アカウント履歴ビュー
@login_required
def account_history_view(request):
    return render(request, 'gt/user_log.html')

# ログ詳細ビュー
@login_required
def log_detail_view(request):
    return render(request, 'gt/user_log_detail.html')




##画面遷移の関数はここより上に書きます

class AccountRegistration(TemplateView):
    template_name = "gt/register.html"

    def get(self, request):
        context = {
            "AccountCreate": False,
            "account_form": AccountForm(),
            "add_account_form": AddAccountForm(),
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        account_form = AccountForm(data=request.POST)
        add_account_form = AddAccountForm(data=request.POST)

        if account_form.is_valid() and add_account_form.is_valid():
            account = account_form.save()
            account.set_password(account.password)
            account.save()

            add_account = add_account_form.save(commit=False)
            add_account.user = account
            add_account.save()

            context = {"AccountCreate": True}
        else:
            logger.error(account_form.errors)
            context = {
                "AccountCreate": False,
                "account_form": account_form,
                "add_account_form": add_account_form
            }
        return render(request, self.template_name, context=context)

# ログインビュー

# ログインビュー
def Login(request):
    if request.method == 'POST':
        username = request.POST.get('userid')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)  # ユーザーをログインさせる
                if request.user.username == 'admin':
                    return HttpResponseRedirect(reverse('gt:admin_top'))
                else:
                    return HttpResponseRedirect(reverse('gt:top'))
            else:
                return HttpResponse("アカウントが有効ではありません")
        else:
            return HttpResponse("ログインIDまたはパスワードが間違っています")

    else:
        return render(request, 'gt/user_login.html')

# ログアウトビュー
@login_required
def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('gt:top'))

# ユーザー情報ビュー
@login_required
def user_info(request):
    account = get_object_or_404(Account, user=request.user)
    return render(request, 'user_info.html', {'account': account})

# ユーザー情報更新ビュー
@login_required
def user_update_view(request):
    if request.method == 'POST':
        form = AccountUpdateForm(request.POST, instance=request.user.account)
        if form.is_valid():
            form.save()
            return redirect('gt:user_info')
    else:
        form = AccountUpdateForm(instance=request.user.account)
    return render(request, 'user_update.html', {'form': form})

@login_required
def user_delete_view(request):
    if request.method == 'POST':
        user = request.user
        logout(request)  # ユーザーをログアウト
        user.delete()  # アカウントを削除
        return redirect('gt:register')  # ログインページにリダイレクト
    else:
        return render(request, 'user_delete.html')



import requests
import json
from django.shortcuts import render
from .forms import LocationForm
from .models import Map
from django.http import JsonResponse

# 管理者用マップ登録ビュー
@login_required
def admin_map_register(request):
    def is_ajax(request):
        return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']

            # ここで外部APIを呼び出し、JSONデータを取得
            api_url = 'https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyA5diRbD4Ex24SsS0_YISzQW5f19mckhf4'
            response = requests.get(api_url, params={'address': address})

            if response.status_code == 200:
                data = response.json()

                # デバックコンソール
                # print("Data:", data)

                location_data = data['results'][0]['geometry']['location']
                lat = location_data['lat']  # 緯度
                lng = location_data['lng']  # 経度

                # 緯度と経度のみを含む辞書を作成
                location_only = {'lat': lat, 'lng': lng}

                # 辞書をJSONにシリアライズ
                json_data = json.dumps(location_only)

                # データベースに保存
                Map.objects.create(name=name, address=address, json_data=json_data)

                show_modal = False
                message_success = "データが保存されました"
                # AJAXリクエストの場合はJsonResponseを返す
                if is_ajax(request):
                    return HttpResponseRedirect(reverse('gt:admin_top'))
                    # return render(request, 'gt/admin_map_register.html', {'form': form})
                # それ以外の場合はテンプレートをレンダリングして返す
                else:
                    show_modal = True
                    return render(request, 'gt/admin_map_register.html', {'form': form,'message': message_success, 'json_data': json_data,'show_modal': show_modal})
            else:
                return JsonResponse({'message': 'APIからデータを取得できませんでした'}, status=400)
        else:
            if is_ajax(request):
                return JsonResponse({'message': 'フォームが無効です'}, ensure_ascii=False, status=400)
            else:
                return render(request, 'gt/admin_map_register.html', {'form': form})
    else:
        form = LocationForm()
        return render(request, 'gt/admin_map_register.html', {'form': form})
