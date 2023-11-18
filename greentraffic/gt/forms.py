from django import forms

class LocationForm(forms.Form):
    name = forms.CharField(label='場所名', max_length=100)
    address = forms.CharField(label='住所', max_length=100)
    latitude = forms.CharField(label='緯度', max_length=100)
    longitude = forms.CharField(label='経度', max_length=100)


from django.contrib.auth.models import User
from .models import Account

# フォームクラス作成
class AccountForm(forms.ModelForm):
    # パスワード入力：非表示対応
    password = forms.CharField(widget=forms.PasswordInput(),label="パスワード")

    class Meta():
        # ユーザー認証
        model = User
        # フィールド指定
        fields = ('username','email','password')
        # フィールド名指定
        labels = {'username':"ユーザーID",'email':"メール"}

class AddAccountForm(forms.ModelForm):
    class Meta():
        # モデルクラスを指定
        model = Account
        fields = ('last_name', 'first_name',  'address', 'gender',)
        labels = {
            'last_name': "苗字",
            'first_name': "名前",
            'address': "住所",  # 住所フィールドのラベル
            'gender': "性別",  # 性別フィールドのラベル
        }