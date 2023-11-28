from django.shortcuts import render,get_object_or_404,HttpResponseRedirect,redirect

from .models import models

# from .forms import LocationForm
# from .models import Map

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

# 管理者用マップ登録ビュー
@login_required
def admin_map_register(request):
    return render(request, 'gt/admin_map_register.html')

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
                if request.user.username == 'kobayashi':
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

