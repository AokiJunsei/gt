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

from .models import Account, MapCar ,MapBike
from .forms import AccountForm, AddAccountForm, AccountDeleteForm, AccountUpdateForm, LocationForm

from django.db import transaction
import requests
import json
import logging
from django.contrib import messages

# ロガーの設定
logger = logging.getLogger(__name__)

# トップページのビュー
def top_page(request):
    return render(request, 'gt/top.html')

# 最安検索のビュー
def user_search_cheap(request):
    return render(request, 'gt/user_search_cheap.html')

# シェアリング検索（車）のビュー
def user_search_share_car(request):
    return render(request, 'gt/user_search_share_car.html')

# シェアリング検索（自転車）のビュー
def user_search_share_bike(request):
    return render(request, 'gt/user_search_share_bike.html')

# 履歴を残す検索のビュー
def user_my_map(request):
    return render(request, 'gt/user_my_map.html')

# 管理者用ユーザー情報閲覧ページのビュー
def admin_user_info(request):
    return render(request, 'gt/admin_user_info.html')

# 管理者用トップページのビュー
@login_required
def admin_top(request):
    map_car = MapCar.objects.all()
    map_bike = MapBike.objects.all()
    return render(request, 'gt/admin_top.html', {'map_car' : map_car, 'map_bike' : map_bike})


# 管理者用マップ登録ビュー
@login_required
def admin_map_register(request):
    message_success = "データが保存されました。"
    alert_API = "APIからデータを取得できませんでした。"
    alert_form = "フォームが無効です。正しく記入してください。"
    none_data = "データを取得できませんでした。正しい住所を入力してください。"
    show_modal = True
    show_alert = True

    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            vehicle_type = form.cleaned_data['vehicle_type']

            # ここで外部APIを呼び出し、JSONデータを取得
            api_url = 'https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyA5diRbD4Ex24SsS0_YISzQW5f19mckhf4'
            response = requests.get(api_url, params={'address': address})

            if response.status_code == 200:
                data = response.json()

                if data['status'] == 'ZERO_RESULTS':
                    return render(request, 'gt/admin_map_register.html', {'form': form,'message': none_data, 'show_alert': show_alert})

                location_data = data['results'][0]['geometry']['location']
                lat = location_data['lat']  # 緯度
                lng = location_data['lng']  # 経度

                # 緯度と経度のみを含む辞書を作成
                location_only = {'lat': lat, 'lng': lng}

                # 辞書をJSONにシリアライズ
                json_data = json.dumps(location_only)

                # データベースに保存
                if vehicle_type == 'car':
                    MapCar.objects.create(name=name, address=address, json_data=json_data)
                elif vehicle_type == 'bike':
                    MapBike.objects.create(name=name, address=address, json_data=json_data)
                return render(request, 'gt/admin_map_register.html', {'form': form,'message': message_success, 'json_data': json_data,'show_modal': show_modal})
            else:
                return render(request, 'gt/admin_map_register.html', {'form': form,'message': alert_API, 'show_alert': show_alert})
        else:
            return render(request, 'gt/admin_map_register.html', {'form': form,'message': alert_form, 'show_alert': show_alert})
    else:
        form = LocationForm()
        return render(request, 'gt/admin_map_register.html', {'form': form})


# 管理者用マップ変更ビュー
@login_required
def admin_map_change(request,vehicle_type, pk):
    # 既存のインスタンスを取得するかどうか判断
    map_change = None
    if pk:
        # 車種タイプに基づいてオブジェクトを取得
        if vehicle_type == 'car':
            map_change = get_object_or_404(MapCar, pk=pk)
        elif vehicle_type == 'bike':
            map_change = get_object_or_404(MapBike, pk=pk)
        else:
            messages.error(request, "不正な車両タイプが指定されました。")
            return redirect('gt:admin_top')
    if map_change:
        form = LocationForm(initial={
            'name': map_change.name,
            'address': map_change.address,
            'vehicle_type': vehicle_type
        })
    else:
        form = LocationForm()

    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            if not map_change or form.cleaned_data['vehicle_type'] != vehicle_type:
                # Delete the old instance if the vehicle type has changed
                if map_change:
                    map_change.delete()
                # Create a new instance based on the form's vehicle_type
                map_change = MapCar() if form.cleaned_data['vehicle_type'] == 'car' else MapBike()

            map_change.address = form.cleaned_data['address']
            # ここで外部APIを呼び出し、JSONデータを取得
            api_url = 'https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyA5diRbD4Ex24SsS0_YISzQW5f19mckhf4'
            response = requests.get(api_url, params={'address': map_change.address})

            if response.status_code == 200:
                with transaction.atomic():
                    data = response.json()
                    location_data = data['results'][0]['geometry']['location']
                    map_change.lat = location_data['lat']  # 緯度
                    map_change.lng = location_data['lng']  # 経度

                    # 緯度と経度のみを含む辞書を作成
                    location_only = {'lat': map_change.lat, 'lng': map_change.lng}

                    # 辞書をJSONにシリアライズ
                    map_change.json_data = json.dumps(location_only)

                    map_change.name = form.cleaned_data['name']
                    map_change.json_data = map_change.json_data
                    map_change.save()

                    message_success = "データが保存されました"
                return render(request, 'gt/admin_map_register.html', {
                    'form': form,
                    'message': message_success,
                    'json_data': map_change.json_data,
                    'show_modal': True
                })
            else:
                alert_API = "APIからデータを取得できませんでした"
                # APIからデータを取得できなかった場合の処理
                return render(request, 'gt/admin_map_change.html', {
                    'form': form,
                    'message': alert_API,
                    'show_alert': True
                })
        else:
            # フォームが無効な場合の処理
            alert_form = "フォームが無効です"
            return render(request, 'gt/admin_map_change.html', {
                'form': form,
                'message': alert_form,
                'show_alert': True
            })
    else:
        # GETリクエストの場合、フォームを既存のデータで初期化
        form = LocationForm(initial={'name': map_change.name, 'address': map_change.address})
        return render(request, 'gt/admin_map_change.html', {'form': form})

# 管理者用マップ削除ビュー
@login_required
def admin_map_delete(request, pk, vehicle_type):
    if vehicle_type == 'car':
        map_delete = get_object_or_404(MapCar, pk=pk)
    elif vehicle_type == 'bike':
        map_delete = get_object_or_404(MapBike, pk=pk)
    else:
        return redirect('gt:admin_top')
    map_delete.delete()
    return redirect(reverse('gt:admin_top'))

# 管理者用マップ詳細ビュー
@login_required
def admin_map_detail(request, pk, vehicle_type):
    if vehicle_type == 'car':
        map_detail = get_object_or_404(MapCar, pk=pk)
    elif vehicle_type == 'bike':
        map_detail = get_object_or_404(MapBike, pk=pk)
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
    user = request.user
    account = user.account

    if request.method == 'POST':
        form = AccountUpdateForm(request.POST, instance=account)
        if form.is_valid():
            # User モデルの更新
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.password = form.cleaned_data['password']
            user.save()

            # Account モデルの更新
            form.save()
            return redirect('gt:user_info')
    else:
        form = AccountUpdateForm(instance=account, initial={'username': user.username, 'email': user.email})

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
