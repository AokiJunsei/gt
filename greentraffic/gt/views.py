from django.shortcuts import render,get_object_or_404,HttpResponseRedirect,redirect

from .models import models

from django.views.generic import TemplateView
from .forms import AccountForm, AddAccountForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Account, Map
from .forms import AccountForm, AddAccountForm, AccountDeleteForm, AccountUpdateForm, LocationForm

import requests
import json
import logging

# ロガーの設定
logger = logging.getLogger(__name__)

# トップページのビュー
def top_page(request):
    return render(request, 'gt/top.html')

# 管理者用トップページのビュー
@login_required
def admin_top(request):
    map_list = Map.objects.all()
    return render(request, 'gt/admin_top.html', {'map_list' : map_list})


# 管理者用マップ変更ビュー
@login_required
def admin_map_change(request, pk):
    map_change = get_object_or_404(Map, pk=pk)
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            map_change.name = form.cleaned_data['name']
            map_change.address = form.cleaned_data['address']

            # ここで外部APIを呼び出し、JSONデータを取得
            api_url = 'https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyA5diRbD4Ex24SsS0_YISzQW5f19mckhf4'
            response = requests.get(api_url, params={'address': map_change.address})

            if response.status_code == 200:
                data = response.json()
                location_data = data['results'][0]['geometry']['location']
                map_change.lat = location_data['lat']  # 緯度
                map_change.lng = location_data['lng']  # 経度

                # 緯度と経度のみを含む辞書を作成
                location_only = {'lat': map_change.lat, 'lng': map_change.lng}

                # 辞書をJSONにシリアライズ
                map_change.json_data = json.dumps(location_only)

                # データベースに保存
                map_change.save()

                message_success = "データが保存されました"
                alert_API = "APIからデータを取得できませんでした"
                alert_form = "フォームが無効です"
                show_modal = True
                show_alert = True
                return render(request, 'gt/admin_map_register.html', {
                    'form': form,
                    'message': message_success,
                    'json_data': map_change.json_data,
                    'show_modal': show_modal
                })
            else:
                # APIからデータを取得できなかった場合の処理
                return render(request, 'gt/admin_map_change.html', {
                    'form': form,
                    'message': alert_API,
                    'show_alert': show_alert
                })
        else:
            # フォームが無効な場合の処理
            return render(request, 'gt/admin_map_change.html', {
                'form': form,
                'message': alert_form,
                'show_alert': show_alert
            })
    else:
        # GETリクエストの場合、フォームを既存のデータで初期化
        form = LocationForm(initial={'name': map_change.name, 'address': map_change.address})
        return render(request, 'gt/admin_map_change.html', {'form': form})

# 管理者用マップ削除ビュー
@login_required
def admin_map_delete(request, pk):
    map_delete = get_object_or_404(Map, pk=pk)
    map_delete.delete()
    return redirect(reverse('gt:admin_top'))

# 管理者用マップ詳細ビュー
@login_required
def admin_map_detail(request, pk):
    map_detail = get_object_or_404(Map, pk=pk)
    return render(request, 'gt/admin_map_detail.html', {'map_detail': map_detail})


# アカウント履歴ビュー
@login_required
def account_history_view(request):
    return render(request, 'gt/user_log.html')

# ログ詳細ビュー
@login_required
def log_detail_view(request):
    return render(request, 'gt/user_log_detail.html')



##画面遷移の関数はここより上に書きます

# 新規登録ビュー
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

def my_view(request):
    if request.user.is_authenticated:
        # 特定のユーザーの場合
        if request.user.username == 'kobayashi':
            return redirect('特定のページのURL名')
        # それ以外のユーザーの場合
        else:
            return redirect('通常のページのURL名')
    else:
        # 未認証の場合
        return redirect('ログインページのURL名')

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

# ユーザー退会ビュー
@login_required
def user_delete_view(request):
    if request.method == 'POST':
        user = request.user
        logout(request)  # ユーザーをログアウト
        user.delete()  # アカウントを削除
        return redirect('gt:register')  # ログインページにリダイレクト
    else:
        return render(request, 'user_delete.html')


# 管理者用マップ登録ビュー
@login_required
def admin_map_register(request):
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

                message_success = "データが保存されました"
                alert_API = "APIからデータを取得できませんでした"
                alert_form = "フォームが無効です"
                show_modal = True
                show_alert = True
                return render(request, 'gt/admin_map_register.html', {'form': form,'message': message_success, 'json_data': json_data,'show_modal': show_modal})
            else:
                return render(request, 'gt/admin_map_register.html', {'form': form,'message': alert_API, 'show_alert': show_alert})
        else:
            return render(request, 'gt/admin_map_register.html', {'form': form,'message': alert_form, 'show_alert': show_alert})
    else:
        form = LocationForm()
        return render(request, 'gt/admin_map_register.html', {'form': form})
