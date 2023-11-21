from django import forms
from django.contrib.auth.models import User
from .models import Account
from django import forms
from django.core.exceptions import ValidationError
import re

class LocationForm(forms.Form):
    name = forms.CharField(label='場所名', max_length=100)
    address = forms.CharField(label='住所', max_length=100)
    latitude = forms.CharField(label='緯度', max_length=100)
    longitude = forms.CharField(label='経度', max_length=100)




# フォームクラス作成
class AccountForm(forms.ModelForm):
    # パスワード入力：非表示対応
    password = forms.CharField(widget=forms.PasswordInput(), label="パスワード")

    class Meta:
        # ユーザー認証
        model = User
        # フィールド指定
        fields = ('username', 'email', 'password')
        # フィールド名指定
        labels = {'username': "ユーザーID", 'email': "メール"}

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError('パスワードは8文字以上である必要があります。')
        if not re.search(r'\d', password):
            raise ValidationError('パスワードには少なくとも1つの数字を含める必要があります。')
        return password

    # 新しい住所関連フィールド
    zipcode = forms.CharField(max_length=7, required=False, label='郵便番号')
    state = forms.CharField(max_length=100, required=False, label='都道府県')
    city = forms.CharField(max_length=100, required=False, label='市区町村')
    address_1 = forms.CharField(max_length=100, required=False, label='番地')
    address_2 = forms.CharField(max_length=100, required=False, label='建物名・部屋番号')

    

# 追加のアカウント情報用のフォーム
class AddAccountForm(forms.ModelForm):
    class Meta:
        # モデルクラスを指定
        model = Account
        # フィールド指定
        fields = ('last_name', 'first_name', 'address', 'zipcode', 'state', 'city', 'address_1', 'address_2', 'gender')
        # フィールド名指定
        labels = {
            'last_name': "苗字",
            'first_name': "名前",
            'address': "住所",
            'zipcode': "郵便番号",
            'state': "都道府県",
            'city': "市区町村",
            'address_1': "番地",
            'address_2': "建物名・部屋番号",
            'gender': "性別",
        }

##########user_delete.htmlのformクラス##########

class AccountDeleteForm(forms.Form):
    confirm_username = forms.CharField(label='Confirm Username', max_length=150)



##########user_update.htmlのformクラス##########

class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['last_name', 'first_name', 'zipcode', 'state', 'city', 'address', 'address_1', 'address_2', 'gender']