from django import forms
from django.contrib.auth.models import User
from .models import Account
from django.core.exceptions import ValidationError
import re
import json


# 日本の都道府県リスト
PREFECTURES = [
    '北海道', '青森県', '岩手県', '宮城県', '秋田県',
    '山形県', '福島県', '茨城県', '栃木県', '群馬県',
    '埼玉県', '千葉県', '東京都', '神奈川県', '新潟県',
    '富山県', '石川県', '福井県', '山梨県', '長野県',
    '岐阜県', '静岡県', '愛知県', '三重県', '滋賀県',
    '京都府', '大阪府', '兵庫県', '奈良県', '和歌山県',
    '鳥取県', '島根県', '岡山県', '広島県', '山口県',
    '徳島県', '香川県', '愛媛県', '高知県', '福岡県',
    '佐賀県', '長崎県', '熊本県', '大分県', '宮崎県',
    '鹿児島県', '沖縄県'
]

# フォームクラス作成
class AccountForm(forms.ModelForm):
    username = forms.CharField(
        max_length=100,
        required=True,
        label='ユーザーID',
        widget=forms.TextInput(attrs={
            'placeholder': '例：test'
        })
    )
    # パスワード入力：非表示対応
    email = forms.CharField(
        max_length=100,
        required=True,
        label='メール',
        widget=forms.TextInput(attrs={
            'placeholder': '例：xxx@xxx.com'
        })
    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={
            'placeholder': '8文字以上数字を含む',
        }),
        label="パスワード" )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'パスワード確認',
        }),
        label="パスワード確認"
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')
        # フィールド名指定
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("ユーザーIDは既に使用されています。")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError('パスワードは8文字以上である必要があります。')
        if not re.search(r'\d', password):
            raise ValidationError('パスワードには少なくとも1つの数字を含める必要があります。')
        return password
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # パスワードが一致するか確認
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'パスワードが一致しません。')

        return cleaned_data


# ユーザー更新フォームクラス作成
class UpdateAccountForm(forms.ModelForm):
    username = forms.CharField(
        max_length=100,
        required=True,
        label='ユーザーID',
        widget=forms.TextInput(attrs={
            'placeholder': '例：test'
        })
    )
    # パスワード入力：非表示対応
    email = forms.CharField(
        max_length=100,
        required=True,
        label='メール',
        widget=forms.TextInput(attrs={
            'placeholder': '例：xxx@xxx.com'
        })
    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={
            'placeholder': '8文字以上数字を含む',
        }),
        label="パスワード" )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'パスワード確認',
        }),
        label="パスワード確認"
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')
        # フィールド名指定
    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError('パスワードは8文字以上である必要があります。')
        if not re.search(r'\d', password):
            raise ValidationError('パスワードには少なくとも1つの数字を含める必要があります。')
        return password
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # パスワードが一致するか確認
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'パスワードが一致しません。')

        return cleaned_data


# 郵便番号の長さを検証するカスタムバリデータ
def validate_zipcode_length(value):
    if len(value) != 7:
        raise ValidationError('郵便番号は7文字でなければなりません。')

# 都道府県バリデーション
def validate_prefecture(value):
    if value not in PREFECTURES:
        raise ValidationError('有効な都道府県を入力してください。')

# 追加のアカウント情報用のフォーム
class AddAccountForm(forms.ModelForm):
    last_name = forms.CharField(
        max_length=100,
        required=True,
        label='苗字',
        widget=forms.TextInput(attrs={
            'placeholder': '例：大原'
        })
    )
    first_name = forms.CharField(
        max_length=100,
        required=True,
        label='名前',
        widget=forms.TextInput(attrs={
            'placeholder': '例：太郎'
        })
    )
    zipcode = forms.CharField(
        max_length=7,
        required=True,
        validators=[validate_zipcode_length],
        widget=forms.TextInput(attrs={
            'placeholder': '例：1018351'
        }),
        label='郵便番号',
    )
    state = forms.CharField(
        max_length=100,
        required=True,
        validators=[validate_prefecture],
        widget=forms.TextInput(attrs={
            'placeholder': '例：東京都 '
        }),
        label='都道府県',
    )
    city = forms.CharField(max_length=100, required=True, label='市区町村',widget=forms.TextInput(attrs={
            'placeholder': '例：千代田区西神田 '
        }),)
    address_1 = forms.CharField(max_length=100, required=True, label='番地',widget=forms.TextInput(attrs={
            'placeholder': '例：2-4-11 '
        }),)
    address_2 = forms.CharField(max_length=100, label='建物名・部屋番号',widget=forms.TextInput(attrs={
            'placeholder': '例：TICビル '
        }),)
    class Meta:
        # モデルクラスを指定
        model = Account

        # フィールド指定
        fields = ('last_name', 'first_name', 'address', 'zipcode', 'state', 'city', 'address_1', 'address_2', 'gender',)
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
    username = forms.CharField(
        max_length=150,
        required=True,
        label='ユーザーID'
    )
    email = forms.EmailField(
        required=True,
        label='メールアドレス'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label="新しいパスワード",
        required= True # 更新の際にはパスワードが必須ではない場合
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(),
        label="パスワード確認",
        required=True  # 更新の際にはパスワードが必須ではない場合
    )
    class Meta:
        model = Account
        fields = [
            'username', 'email', 'last_name', 'first_name', 
            'zipcode', 'state', 'city', 'address_1', 
            'address_2', 'gender', 'password', 'confirm_password'
        ]
        labels = {
            'last_name': "苗字",
            'first_name': "名前",
            'zipcode': "郵便番号",
            'state': "都道府県",
            'city': "市区町村",
            'address_1': "番地",
            'address_2': "建物名・部屋番号",
            'gender': "性別",
        }


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(pk=self.instance.user.pk).exists():
            raise ValidationError('メールアドレスは既に使用されています。')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if len(password) < 8:
                raise ValidationError('パスワードは8文字以上である必要があります。')
            if not re.search(r'\d', password):
                raise ValidationError('パスワードには少なくとも1つの数字を含める必要があります。')
            if password != confirm_password:
                self.add_error('confirm_password', 'パスワードが一致しません。')
            return cleaned_data

class LocationForm(forms.Form):
    name = forms.CharField(label='登録名', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '例：東京都'})    )
    address = forms.CharField(label='住所', max_length=200, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '例：東京駅 '}))
    vehicle_type = forms.ChoiceField(label='種類',choices=[('car', '自動車'), ('bike', '自転車',)])

class SpotForm(forms.Form):
    name = forms.CharField(label='登録名', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '例：東京都 '}))
    address = forms.CharField(label='住所', max_length=200, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '例：東京駅 '}))

class RouteSearchForm(forms.Form):
    start = forms.CharField(label='出発地', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例：東京駅 '}), required=False)
    end = forms.CharField(label='目的地', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例：大宮駅 '}), required=False)
    travel_mode = forms.ChoiceField(
        choices=[
            ('DRIVING', '自動車'),
            ('WALKING', '徒歩'),
            ('BICYCLING', '自転車'),
        ]
    )
    start_spot = forms.ChoiceField(choices=[('', '---')], required=False, label='出発地スポット')
    end_spot = forms.ChoiceField(choices=[('', '---')], required=False, label='目的地スポット')

    def __init__(self, *args, **kwargs):
        user_spots = kwargs.pop('user_spots', [])
        super(RouteSearchForm, self).__init__(*args, **kwargs)

        # 初期選択肢を含むスポットの選択肢を作成
        spot_choices = [('', '---')]  # 初期値として空の選択肢を追加
        for spot in user_spots:
            spot_label = f"{spot['spot_name']} - {spot['address']}"  # スポット名と住所を組み合わせたラベル
            # JSON文字列をオプションの値としてセット
            spot_value = json.dumps({
                'lat': spot['json_data']['lat'],
                'lng': spot['json_data']['lng']
            })
            spot_choices.append((spot_value, spot_label))
        self.fields['start_spot'].choices = spot_choices
        self.fields['end_spot'].choices = spot_choices
