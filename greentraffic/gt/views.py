from django.shortcuts import render,get_object_or_404,HttpResponseRedirect,redirect

from django.views.generic import TemplateView
from .forms import AccountForm, AddAccountForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Account, MapCar ,MapBike ,Spot ,SearchHistory ,User
from .forms import AccountForm, AddAccountForm, LocationForm ,SpotForm,RouteSearchForm ,UpdateAccountForm
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
import requests
import json
import logging
from django.contrib import messages
from django.core.mail import send_mail

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone
from django.contrib.auth import update_session_auth_hash
from django.core.serializers.json import DjangoJSONEncoder

from django.db.models import Count
from django.db.models.functions import TruncMonth

from django.conf import settings
from django.views.decorators.http import require_http_methods

# 電車のfetchの関数
@require_http_methods(["GET"])
def fetch_jorudan_cheap_route(request):
    api_key = settings.JOULDAN_API_KEY

    # フロントエンドから渡されるクエリパラメータを取得
    start = request.GET.get('start')
    end = request.GET.get('end')
    waypoint1 = request.GET.get('waypoint1')
    waypoint2 = request.GET.get('waypoint2')
    departureDate = request.GET.get('departureDate')
    departureTime = request.GET.get('departureTime')
    sort = request.GET.get('sort')

    base_url = 'https://cloud.jorudan.biz/api/gv'
    params = {
        'ak': api_key,
        'f' : 1,
        'rm' : 'sr',
        'eki1' : start,
        'eki2' : end,
        'kbn1' : 'R',
        'date' : departureDate,
        'time' : departureTime,
        'opt1' : 0,
        'opt2' : 0,
        'opt3' : 1,
        'opt4' : 0,
        'max' : 8,
        'sort' : sort,
        'trtm' : 3
    }
    response = requests.get(base_url, params=params)
    return JsonResponse(response.json())

# ロガーの設定
logger = logging.getLogger(__name__)

# トップページのビュー(車)
def top_page(request):
    # APIキーを取得
    api_key = settings.GOOGLE_API_KEY
    context = {
        "api_key" : api_key
    }
    return render(request, 'gt/user_search_car.html', context)

# 徒歩の検索
def user_search_walk(request):
    # APIキーを取得
    api_key = settings.GOOGLE_API_KEY
    context = {
        "api_key" : api_key
    }
    return render(request, 'gt/user_search_walk.html', context)

# 自転車の検索
def user_search_bike(request):
    # APIキーを取得
    api_key = settings.GOOGLE_API_KEY
    context = {
        "api_key" : api_key
    }
    return render(request, 'gt/user_search_bike.html', context)

# 電車最短検索のビュー
def user_search_short(request):
    # APIキーを取得
    api_key = settings.GOOGLE_API_KEY
    context = {
        "api_key" : api_key
    }
    return render(request, 'gt/user_search_short.html', context)

# 電車最安検索のビュー
def user_search_cheap(request):
    # APIキーを取得
    api_key = settings.GOOGLE_API_KEY
    context = {
        "api_key" : api_key,
    }
    return render(request, 'gt/user_search_cheap.html', context)

# シェアリング検索（車）のビュー
def user_search_share_car_car(request):
    # APIキーを取得
    api_key = settings.GOOGLE_API_KEY
    context = {
        "api_key" : api_key
    }
    return render(request, 'gt/user_search_share_car_car.html', context)
# シェアリング検索（自転車）のビュー
def user_search_share_car_bike(request):
    # APIキーを取得
    api_key = settings.GOOGLE_API_KEY
    context = {
        "api_key" : api_key
    }
    return render(request, 'gt/user_search_share_car_bike.html', context)
# シェアリング検索（徒歩）のビュー
def user_search_share_car_walk(request):
    # APIキーを取得
    api_key = settings.GOOGLE_API_KEY
    context = {
        "api_key" : api_key
    }
    return render(request, 'gt/user_search_share_car_walk.html', context)
# シェアリング検索（車１）のビュー
def user_search_share_bike_car(request):
    # APIキーを取得
    api_key = settings.GOOGLE_API_KEY
    context = {
        "api_key" : api_key
    }
    return render(request, 'gt/user_search_share_bike_car.html', context)
# シェアリング検索（自転車１）のビュー
def user_search_share_bike_bike(request):
    # APIキーを取得
    api_key = settings.GOOGLE_API_KEY
    context = {
        "api_key" : api_key
    }
    return render(request, 'gt/user_search_share_bike_bike.html', context)
# シェアリング検索（徒歩１）のビュー
def user_search_share_bike_walk(request):
    # APIキーを取得
    api_key = settings.GOOGLE_API_KEY
    context = {
        "api_key" : api_key
    }
    return render(request, 'gt/user_search_share_bike_walk.html', context)

# 管理者用トップページのビュー
@login_required
def admin_top(request):
    map_car = MapCar.objects.all()
    map_bike = MapBike.objects.all()
    return render(request, 'gt/admin_top.html', {'map_car' : map_car, 'map_bike' : map_bike})


# 管理者用マップ登録ビュー
@login_required
def admin_map_register(request):
    message = None
    show_modal = False
    show_alert = False
    json_data = None
    # APIキーを取得
    api_key = settings.GOOGLE_API_KEY

    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            vehicle_type = form.cleaned_data['vehicle_type']

            api_url = 'https://maps.googleapis.com/maps/api/geocode/json'

            response = requests.get(api_url, params={'address': address, 'key': api_key})

            if response.status_code == 200:
                data = response.json()

                if data['status'] == 'ZERO_RESULTS':
                    message = "データを取得できませんでした。正しい住所を入力してください。"
                    show_alert = True
                else:
                    location_data = data['results'][0]['geometry']['location']
                    lat = location_data['lat']
                    lng = location_data['lng']
                    location_only = {'lat': lat, 'lng': lng}
                    json_data = json.dumps(location_only)

                    # データベースに保存
                    if vehicle_type == 'car':
                        MapCar.objects.create(name=name, address=address, json_data=json_data)
                    elif vehicle_type == 'bike':
                        MapBike.objects.create(name=name, address=address, json_data=json_data)

                    message = "データが保存されました。"
                    show_modal = True
            else:
                message = "APIからデータを取得できませんでした。"
                show_alert = True
        else:
            message = "フォームが無効です。正しく記入してください。"
            show_alert = True
    else:
        form = LocationForm()

    context = {
        'form': form,
        'message': message,
        'show_modal': show_modal,
        'show_alert': show_alert,
        'json_data': json_data or "null",
        'api_key': api_key if api_key is not None else settings.GOOGLE_API_KEY
    }
    return render(request, 'gt/admin_map_register.html', context)



# 管理者用マップ変更ビュー
@login_required
def admin_map_change(request,vehicle_type, pk):
    # APIキーを取得
    api_key = settings.GOOGLE_API_KEY
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
            api_url = 'https://maps.googleapis.com/maps/api/geocode/json'
            response = requests.get(api_url, params={'address': map_change.address,'key': api_key})

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
                return render(request, 'gt/admin_map_change.html', {
                    'form': form,
                    'message': message_success,
                    'json_data': map_change.json_data,
                    'show_modal': True,
                    'api_key': api_key
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
        return render(request, 'gt/admin_map_change.html',  {'form': form, 'api_key': api_key})

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

    # APIキーを取得
    api_key = settings.GOOGLE_API_KEY
    context = {
        'map_detail': map_detail,
        'api_key': api_key
    }
    return render(request, 'gt/admin_map_detail.html', context)

# ジオコードAPIの関数
def get_geocode(address):
    # APIキーを取得
    api_key = settings.GOOGLE_API_KEY # 適切なAPIキーに置き換えてください
    params = {'address': address, 'key': api_key}
    response = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=params)

    if response.status_code == 200:
        data = response.json()
        if data['results']:
            location = data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
    return None, None

# 新規登録ビュー
class AccountRegistration(TemplateView):
    template_name = "gt/user_register.html"
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
        username = request.POST.get('username')  # ユーザーネームフィールドの名前に応じて変更

        if account_form.is_valid() and add_account_form.is_valid():
        # ユーザーネームの重複チェック
            if User.objects.filter(username=username).exists():
                return render(request, self.template_name, {
                    "account_form": account_form,
                    "add_account_form": add_account_form,
                    "error_message": "同じ名前で登録されています。"
                })

            request.session['account_data'] = account_form.cleaned_data
            request.session['add_account_data'] = add_account_form.cleaned_data


            # アドレスから緯度経度を取得
            full_address = f"{add_account_form.cleaned_data['state']} {add_account_form.cleaned_data['city']} {add_account_form.cleaned_data['address_1']}"
            latitude, longitude = get_geocode(full_address)

            if latitude is None or longitude is None:
                context = {
                    "AccountCreate": False,
                    "account_form": account_form,
                    "add_account_form": add_account_form,
                    "error_message": "住所から緯度経度の取得に失敗しました。"
                }
                return render(request, self.template_name, context=context)

            # 緯度経度をセッションのデータに追加
            add_account_data = add_account_form.cleaned_data
            add_account_data['latitude'] = latitude
            add_account_data['longitude'] = longitude
            request.session['account_data'] = account_form.cleaned_data
            request.session['add_account_data'] = add_account_data

            # 一意の認証トークンを生成し、メール送信
            token = default_token_generator.make_token(User())
            self.send_activation_email(request, account_form.cleaned_data['email'], account_form.cleaned_data['username'], token)

            # メール確認ページへのリダイレクト
            context = {"AccountCreate": True}
        else:
            context = {
                "AccountCreate": False,
                "account_form": account_form,
                "add_account_form": add_account_form,
                "error_message": "確認メール送信に失敗しました。登録内容を確認してください。"
            }
        return render(request, self.template_name, context=context)

    def send_activation_email(self, request, email, username, token):
        verification_url = reverse('gt:activate', kwargs={'username': username, 'token': token})
        link = request.build_absolute_uri(verification_url)
        message = (
            f'拝啓 {username} 様、\n\n'
            'Green Trafficへようこそ。\n'
            'ご登録いただいたメールアドレスの認証をお願いいたします。\n'
            '下記のリンクをクリックして、メール認証を完了してください。\n\n'
            f'メール認証リンク: {link}\n\n'
            'メール認証を完了すると、すぐにGreen Trafficの全機能をご利用いただけます。\n'
            'もし、このメールに覚えがない場合は、このメールを無視していただくか、当社のサポートチームまでご連絡をお願いいたします。\n\n'
            '敬具,\n'
            'Green Traffic サポートチーム'
        )
        send_mail('【Green Traffic】メールアドレスの認証について', message, settings.EMAIL_HOST_USER, [email])


def activate_account(request, username, token):
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        if user.is_active:
            # 既にアクティブな場合、top.htmlにエラーメッセージを表示
            context = {'registered': 'このアカウントは既に登録されています。'}
            return render(request, 'user_login.html', context)
    if 'account_data' in request.session and 'add_account_data' in request.session:
        account_data = request.session['account_data']
        add_account_data = request.session['add_account_data']
        if default_token_generator.check_token(User(), token):
            user = User.objects.create_user(
                username=account_data['username'],
                email=account_data['email'],
                password=account_data['password']
            )
            user.is_active = True
            user.save()
            account = Account(
                user=user,
                last_name=add_account_data['last_name'],
                first_name=add_account_data['first_name'],
                zipcode=add_account_data.get('zipcode', ''),
                state=add_account_data.get('state', ''),
                city=add_account_data.get('city', ''),
                address=add_account_data.get('address', ''),
                address_1=add_account_data.get('address_1', ''),
                address_2=add_account_data.get('address_2', ''),
                gender=add_account_data.get('gender', '未選択'),
                latitude=add_account_data.get('latitude'),
                longitude=add_account_data.get('longitude'),
            )
            account.save()
            del request.session['account_data']
            del request.session['add_account_data']
            return redirect('gt:registration_complete')
        else:
            return render(request, 'gt:top', {'エラーメッセージ': '無効なトークンです。'})

def registration_complete(request):
    return render(request, 'registration_complete.html')


def Login(request):
    error_message = None  # エラーメッセージの初期化

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
                error_message = "アカウントが有効ではありません"
        else:
            # ログイン試行時に、is_activeがFalseの場合はメール確認を促す
            if user is not None and not user.is_active:
                error_message = "メールアドレスを確認し、アカウントを有効化してください。"
            else:
                error_message = "ログインIDまたはパスワードが間違っています"

    return render(request, 'gt/user_login.html', {'error_message': error_message})


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
        user_form = UpdateAccountForm(request.POST, instance=user)
        account_form = AddAccountForm(request.POST, instance=account)
        if user_form.is_valid() and account_form.is_valid():
            user = user_form.save(commit=False)
            if 'password' in user_form.cleaned_data and user_form.cleaned_data['password']:
                user.set_password(user_form.cleaned_data['password'])  # パスワードが提供された場合のみ更新
            user.save()
            update_session_auth_hash(request, user)

            # 住所が更新されたかをチェック
            account_modified = account_form.save(commit=False)
            if account_form.has_changed() and 'zipcode' in account_form.changed_data:
                # 緯度経度の取得
                full_address = f"{account_modified.state} {account_modified.city} {account_modified.address_1}"
                lat, lng = get_geocode(full_address)
                if lat is not None and lng is not None:
                    account_modified.latitude = lat
                    account_modified.longitude = lng
                else:
                    account_form.add_error(None, "住所に基づいた緯度経度の取得に失敗しました。")
                    return render(request, 'user_update.html', {'user_form': user_form, 'account_form': account_form})

            account_modified.save()
            return redirect('gt:user_info')
    else:
        user_form = AccountForm(instance=user, initial={'username': user.username, 'email': user.email})
        account_form = AddAccountForm(instance=account)

    return render(request, 'user_update.html', {'user_form': user_form, 'account_form': account_form})

# ユーザー退会ビュー
@login_required
def user_delete_view(request):
    if request.method == 'POST':
        user = request.user
        logout(request)  # ユーザーをログアウト
        user.delete()  # アカウントを削除
        return redirect('gt:top')  # ログインページにリダイレクト
    else:
        return render(request, 'user_delete.html')

# スポット一覧のビュー
@login_required
def user_spot_list(request):
    if request.user.is_authenticated:
        try:
            account_instance = Account.objects.get(user=request.user)
            all_user_spots = Spot.objects.filter(account=account_instance)  # all_user_spotsに変更
        except ObjectDoesNotExist:
            all_user_spots = None  # all_user_spotsに変更
    else:
        all_user_spots = None  # all_user_spotsに変更

    # ページネーションの設定
    page = request.GET.get('page', 1)  # URLからページ番号を取得
    paginator = Paginator(all_user_spots, 10)  # 1ページに表示するアイテム数を設定
    try:
        user_spots = paginator.page(page)
    except PageNotAnInteger:
        # ページが整数でない場合、1ページ目を取得
        user_spots = paginator.page(1)
    except EmptyPage:
        # ページが範囲外の場合、最終ページを取得
        user_spots = paginator.page(paginator.num_pages)

    return render(request,'user_spot_list.html', {'user_spots': user_spots, 'is_paginated': True if paginator.num_pages > 1 else False, 'page_obj': user_spots})


# スポット登録ビュー
@login_required
def user_spot_register(request):
    account = Account.objects.get(user=request.user)
    form = SpotForm(request.POST or None)
    # APIキーを取得
    api_key = settings.GOOGLE_API_KEY

    if request.method == 'POST' and form.is_valid():
        name = form.cleaned_data['name']
        address = form.cleaned_data['address']

        # Google Maps Geocoding APIを使用して住所から緯度経度を取得
        api_url = 'https://maps.googleapis.com/maps/api/geocode/json'
        response = requests.get(api_url, params={'address': address, 'key': api_key})

        if response.status_code == 200:
            data = response.json()

            if data['status'] == 'ZERO_RESULTS':
                message = "データを取得できませんでした。正しい住所を入力してください。"
                show_alert = True
                return render(request, 'gt/user_spot_register.html', {
                    'form': form,
                    'message': message,
                    'show_alert': show_alert,
                    'api_key': api_key
                })

            location_data = data['results'][0]['geometry']['location']
            json_data = json.dumps({'lat': location_data['lat'], 'lng': location_data['lng']})

            # データベースに保存
            Spot.objects.create(spot_name=name, address=address, json_data=json_data, account=account)
            message = "データが保存されました"
            show_modal = True
            return render(request, 'gt/user_spot_register.html', {
                'form': form,
                'message': message,
                'json_data': json_data,
                'show_modal': show_modal,
                'api_key': api_key
            })
        else:
            message = "APIからデータを取得できませんでした"
            show_alert = True
            return render(request, 'gt/user_spot_register.html', {
                'form': form,
                'message': message,
                'show_alert': show_alert,
                'api_key': api_key
            })

    return render(request, 'gt/user_spot_register.html', {'form': form, 'api_key': api_key})


# スポット変更ビュー
@login_required
def user_spot_change(request, pk):
    spot_change = get_object_or_404(Spot, pk=pk)
    form = SpotForm(request.POST or None)
    account = Account.objects.get(user = request.user)

    # APIキーを取得
    api_key = settings.GOOGLE_API_KEY

    if request.method == 'POST' and form.is_valid():
        spot_change.spot_name = form.cleaned_data['name']
        spot_change.address = form.cleaned_data['address']
        spot_change.account = account
        message_success = "データが保存されました"
        alert_API = "APIからデータを取得できませんでした"
        show_modal = True
        show_alert = True

        # ここで外部APIを呼び出し、JSONデータを取得
        api_url = 'https://maps.googleapis.com/maps/api/geocode/json'
        response = requests.get(api_url, params={'address': spot_change.address,'key':api_key})

        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'OK':
                location_data = data['results'][0]['geometry']['location']
                spot_change.lat = location_data['lat']  # 緯度
                spot_change.lng = location_data['lng']  # 経度

                # 緯度と経度のみを含む辞書を作成
                location_only = {'lat': spot_change.lat, 'lng': spot_change.lng}

                # 辞書をJSONにシリアライズ
                spot_change.json_data = json.dumps(location_only)

                # データベースに保存
                spot_change.save()

                return render(request, 'gt/user_spot_change.html', {
                    'form': form,
                    'message': message_success,
                    'json_data': spot_change.json_data,
                    'show_modal': show_modal,
                    'api_key': api_key
                })
            else:
                message_alert = "APIからデータを取得できませんでした"
                return render(request, 'gt/user_spot_change.html', {
                    'form': form,
                    'message': message_alert,
                    'show_alert': True,
                    'api_key': api_key
                })
        else:
            # APIからデータを取得できなかった場合の処理
            return render(request, 'gt/user_spot_change.html', {
                'form': form,
                'message': alert_API,
                'show_alert': True,
                'api_key': api_key
            })
    else:
        # GETリクエストの場合、フォームを既存のデータで初期化
        form = SpotForm(initial={'name': spot_change.spot_name, 'address': spot_change.address})
        return render(request, 'gt/user_spot_change.html', {
            'form': form,
            'api_key': api_key
        })


# スポット削除ビュー
@login_required
def user_spot_delete(request, pk):
    spot_delete = get_object_or_404(Spot, pk=pk)
    spot_delete.delete()
    return redirect(reverse('gt:user_spot_list'))


# スポット詳細ビュー
@login_required
def user_spot_detail(request, pk):
    spot_detail = get_object_or_404(Spot, pk=pk)
    # APIキーを取得
    api_key = settings.GOOGLE_API_KEY
    context = {
        'spot_detail': spot_detail,
        'api_key': api_key
    }
    return render(request, 'gt/user_spot_detail.html', context)


#内部API
def get_accounts(request):
    if request.method == 'GET':
        accounts = Account.objects.all().values()

        return JsonResponse(list(accounts), safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405 ,safe=False)

def get_search_histories(request):
    if request.method == 'GET':
        search_histories = SearchHistory.objects.all().values()

        return JsonResponse(list(search_histories), safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405 ,safe=False)

def get_spots(request):
    if request.method == 'GET':
        spots = Spot.objects.all().values()

        return JsonResponse(list(spots), safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405 ,safe=False)

def get_map_cars(request):
    if request.method == 'GET':
        map_cars = MapCar.objects.all().values('map_id','name','address','json_data')

        return JsonResponse(list(map_cars), safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405 ,safe=False)

def get_map_bikes(request):
    if request.method == 'GET':
        map_bikes = MapBike.objects.all().values()

        return JsonResponse(list(map_bikes), safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405 ,safe=False)

# 履歴を残すタイプの検索
@login_required
def user_my_map(request):
    # APIキーを取得
    api_key = settings.GOOGLE_API_KEY
    account = Account.objects.get(user=request.user)
    # スポット情報を取得し、json_dataを適切にデコード
    user_spots = []
    for spot in Spot.objects.filter(account=account).values('spot_name', 'address', 'json_data'):
        try:
            spot['json_data'] = json.loads(spot['json_data']) if isinstance(spot['json_data'], str) else spot['json_data']
            user_spots.append(spot)
        except json.JSONDecodeError as e:
            print("JSONデコードエラー:", e)  # デバッグ情報を出力

    # Accountの緯度経度をスポットの一覧に追加
    user_spots.append({
        'spot_name': '自宅',
        'address': f"{account.state} {account.city} {account.address_1} {account.address_2}",
        'json_data': {
            'lat': float(account.latitude) if account.latitude is not None else None,
            'lng': float(account.longitude) if account.longitude is not None else None
        }
    })

    spots_json = json.dumps(user_spots, cls=DjangoJSONEncoder)

    # 初期値の設定
    initial = {}
    log_id = request.GET.get('log_id')
    if log_id:
        log_detail = get_object_or_404(SearchHistory, pk=log_id, account=account)
        initial = {
            'start': log_detail.start_location,
            'end': log_detail.end_location,
            'travel_mode': log_detail.travel_mode,
        }

    # POSTリクエストの処理
    if request.method == 'POST':
        form = RouteSearchForm(request.POST, user_spots=list(user_spots))
        if form.is_valid():
            start_spot_json = form.cleaned_data.get('start_spot')
            end_spot_json = form.cleaned_data.get('end_spot')
            start = end = travel_mode = None

            try:
            # スポット情報のデコード
                start_spot_label = end_spot_label = None
                if start_spot_json:
                    start_spot = json.loads(start_spot_json.replace("'", '"'))
                    start = f"{start_spot['lat']}, {start_spot['lng']}"
                    start_spot_label = dict(form.fields['start_spot'].choices).get(start_spot_json)
                else:
                    start = form.cleaned_data.get('start')

                if end_spot_json:
                    end_spot = json.loads(end_spot_json.replace("'", '"'))
                    end = f"{end_spot['lat']}, {end_spot['lng']}"
                    end_spot_label = dict(form.fields['end_spot'].choices).get(end_spot_json)
                else:
                    end = form.cleaned_data.get('end')

                travel_mode = form.cleaned_data.get('travel_mode')

                # 検索履歴をデータベースに保存
                SearchHistory.objects.create(
                    account=account,
                    search_query=f"{start} から {end}",
                    start_location=start,
                    end_location=end,
                    start_spot_label=start_spot_label,
                    end_spot_label=end_spot_label,
                    travel_mode=travel_mode,
                    search_datetime=timezone.now()
                )
            except json.JSONDecodeError as e:
                # JSON解析エラーが発生した場合の処理
                print("JSON解析エラー:", e)
                form.add_error(None, "JSON形式が不正です。")

            context = {
                'form': form,
                'start': start,
                'end': end,
                'travel_mode': travel_mode,
                'submitted': True,
                'spots_json': spots_json,
                'api_key': api_key,
            }
        else:
            # フォームが有効でない場合の処理
            context = {
                'form': form,
                'spots_json': spots_json ,
                'api_key': api_key
            }
    else:
        # GETリクエストの処理
        form = RouteSearchForm(initial=initial, user_spots=list(user_spots))
        context = {
            'form': form,
            'spots_json': spots_json,
            'api_key': api_key
        }

    return render(request, 'gt/user_my_map.html', context)

# アカウント履歴ビュー
@login_required
def account_history_view(request):
    # ログインしているユーザーの検索履歴を取得
    search_history_list = SearchHistory.objects.filter(account=request.user.account).order_by('-search_datetime')

    # ページネーターの設定
    paginator = Paginator(search_history_list, 5)  # 1ページに5項目を表示
    page = request.GET.get('page', 1)
    try:
        search_histories = paginator.page(page)
    except PageNotAnInteger:
        search_histories = paginator.page(1)
    except EmptyPage:
        search_histories = paginator.page(paginator.num_pages)

    # テンプレートに渡す
    return render(request, 'gt/user_log.html', {
        'search_histories': search_histories,
        'is_paginated': True if paginator.num_pages > 1 else False, 
        'page_obj': search_histories
    })



# ログ詳細ビュー
@login_required
def log_detail_view(request, pk):
    log_detail = get_object_or_404(SearchHistory, pk=pk)
    # APIキーを取得
    api_key = settings.GOOGLE_API_KEY
    context = {
        'api_key' : api_key,
        'log_detail' : log_detail
    }
    return render(request, 'gt/user_log_detail.html', context)

# ログ削除ビュー
@login_required
def log_delete_view(request, pk):
    log_delete = get_object_or_404(SearchHistory, pk=pk)
    log_delete.delete()
    return redirect(reverse('gt:account_history'))

# 管理者用ユーザー情報閲覧ページのビュー
@login_required
def admin_user_info(request):
    # APIキーを取得
    api_key = settings.GOOGLE_API_KEY

    # 地理的分布の統計
    state_counts = Account.objects.values('state').exclude(state='').annotate(count=Count('state')).order_by('-count')
    # アカウント作成日の統計（月別）
    creation_dates = User.objects \
                        .annotate(month=TruncMonth('date_joined')) \
                        .values('month') \
                        .annotate(count=Count('id')) \
                        .order_by('month')

    # 地理的座標の分析
    coordinates_data = Account.objects.exclude(latitude=None).exclude(longitude=None).annotate(count=Count('id')).values('latitude', 'longitude', 'count')

    # データをJSON形式でコンテキストに渡す
    context = {
        'state_counts': json.dumps(list(state_counts), cls=DjangoJSONEncoder),
        'creation_dates': json.dumps(list(creation_dates), cls=DjangoJSONEncoder),
        'coordinates_data': json.dumps(list(coordinates_data), cls=DjangoJSONEncoder),
        'google_maps_api_key': api_key,
    }
    return render(request, 'admin_user_info.html', context)

# お店検索
@login_required
def user_my_map_shop(request):
    # APIキーを取得
    api_key = settings.GOOGLE_API_KEY
    context = {
        "api_key" : api_key
    }
    return render(request, 'user_my_map_shop.html', context)