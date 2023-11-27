from django.shortcuts import render,get_object_or_404,HttpResponseRedirect,redirect

from .models import models


from .forms import LocationForm
from .models import Map

from django.views.generic import TemplateView
from .forms import AccountForm, AddAccountForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import logging

from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .forms import AccountDeleteForm
from .forms import AccountUpdateForm
from .models import Account

logger = logging.getLogger(__name__)


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
    return render(request, 'user_login.html')





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

#ログイン

def Login(request):
    # POST
    if request.method == 'POST':
        # フォーム入力のユーザーID・パスワード取得
        ID = request.POST.get('userid')
        Pass = request.POST.get('password')

        # Djangoの認証機能
        user = authenticate(request,username=ID, password=Pass)

        # ユーザー認証
        if user:
            #ユーザーアクティベート判定
            if user.is_active:
                # ログイン
                login(request,user)
                # ホームページ遷移
                return HttpResponseRedirect(reverse('gt:top'))
            else:
                # アカウント利用不可
                return HttpResponse("アカウントが有効ではありません")
        # ユーザー認証失敗
        else:
            return HttpResponse("ログインIDまたはパスワードが間違っています")
    # GET
    else:
        return render(request, 'gt/user_login.html')


#ログアウト
@login_required
def Logout(request):
    logout(request)
    # ログイン画面遷移
    return HttpResponseRedirect(reverse('gt:top'))



def index(request):
    # ユーザーがログインしているかどうかをテンプレートに渡すことができます
    is_authenticated = request.user.is_authenticated
    params = {"UserID": request.user, "is_authenticated": is_authenticated}
    return render(request, "gt/top.html", context=params)

# views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Account
from .forms import AccountForm, AccountDeleteForm

@login_required
def user_info(request):
    account = get_object_or_404(Account, user=request.user)
    return render(request, 'user_info.html', {'account': account})

@login_required
def user_update_view(request):
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=request.user.account)
        if form.is_valid():
            form.save()
            return redirect('gt:user_info')
    else:
        form = AccountForm(instance=request.user.account)
    return render(request, 'user_update.html', {'form': form})

@login_required
def user_delete_view(request):
    if request.method == 'POST':
        form = AccountDeleteForm(request.POST, instance=request.user.account)
        if form.is_valid():  # Delete form doesn't need validation in most cases
            request.user.account.delete()
            request.user.delete()
            return redirect('gt:login')  # Or wherever you want to redirect after deletion
    else:
        form = AccountDeleteForm(instance=request.user.account)
    return render(request, 'user_delete_confirm.html', {'form': form})
