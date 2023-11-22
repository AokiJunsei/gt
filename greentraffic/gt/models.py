from django.db import models
from django.contrib.auth.models import User
# アカウントテーブル
class Account(models.Model):
    # account_id = models.AutoField(primary_key=True, verbose_name="アカウントID")
    # name = models.CharField(max_length=100, verbose_name="お名前")
    # password = models.CharField(max_length=100, verbose_name="パスワード")
    # address = models.CharField(max_length=100, verbose_name="住所")
    # telephone_number = models.CharField(max_length=12, verbose_name="電話番号", help_text="ハイフンあり")
    # created = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    # last_updated = models.DateTimeField(auto_now=True, verbose_name="最終更新日時")
    # flag = models.BooleanField(default=False, verbose_name="管理職flag", help_text="admin垢ならTrueに変更")
    # status = models.BooleanField(default=False, verbose_name="アカウントステータス", help_text="ログアウト時にfalse、ログイン時にTrue")
    # link = models.CharField(max_length=1000, verbose_name="SNSプロフィールリンク", blank=True, null=True)

    # ユーザー認証のインスタンス(1対1関係)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=7, blank=True)
    state = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=255, blank=True)
    address_1 = models.CharField(max_length=100, blank=True)
    address_2 = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=1, choices=[('M', '男'), ('F', '女'), ('O', 'その他')], blank=True)  # 性別
    walking = models.CharField(max_length=100, choices=[('Fast', 'はやい'), ('Normal', 'ふつう'), ('Slow', 'おそい')], blank=True)  #徒歩
    def __str__(self):
        return self.user.username

    # def __str__(self):
    #     return f"{self.account_id} - {self.name}"

    # class Meta:
    #     db_table = "GT001_account"
    #     verbose_name = "アカウントテーブル"


# 検索履歴テーブル
class SearchHistory(models.Model):
    history_id = models.AutoField(primary_key=True, verbose_name="履歴ID")
    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="アカウントID")
    search_result = models.CharField(max_length=100, verbose_name="検索結果")
    search_datetime = models.DateTimeField(auto_now_add=True, verbose_name="検索日時")
    search_query = models.CharField(max_length=100, verbose_name="検索クエリ")
    search_type = models.CharField(max_length=100, verbose_name="検索の種類")

    def __str__(self):
        return f"{self.history_id} - {self.account.name} - {self.search_result}"

    # class Meta:
    #     db_table = "GT002_search_history"
    #     verbose_name = "検索履歴テーブル"


# スポットテーブル
class Spot(models.Model):
    spot_id = models.AutoField(primary_key=True, verbose_name="スポットID")
    spot_name = models.CharField(max_length=100, verbose_name="スポット名")
    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="アカウントID")
    category = models.CharField(max_length=100, verbose_name="カテゴリ")
    address = models.CharField(max_length=100, verbose_name="住所")
    contact_info = models.CharField(max_length=300, verbose_name="連絡先情報")
    fee_info = models.CharField(max_length=100, verbose_name="料金情報", blank=True, null=True)
    business_hours = models.CharField(max_length=100, verbose_name="営業時間", blank=True, null=True)
    latitude = models. CharField(max_length=100, verbose_name="緯度")
    longitude = models. CharField(max_length=100, verbose_name="経度")

    def __str__(self):
        return f"{self.spot_id} - {self.spot_name}"

    # class Meta:
    #     db_table = "GT003_spot"
    #     verbose_name = "スポットテーブル"


# マップテーブル
class Map(models.Model):
    map_id = models.AutoField(primary_key=True, verbose_name="マップID")
    location_name = models.CharField(max_length=100, verbose_name="位置名")
    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="アカウントID")
    category = models.CharField(max_length=100, verbose_name="カテゴリ")
    address = models.CharField(max_length=100, verbose_name="住所")
    latitude = models. CharField(max_length=100, verbose_name="緯度")
    longitude = models. CharField(max_length=100, verbose_name="経度")
    
    def __str__(self):
        return f"{self.map_id} - {self.location_name}"
    
    # class Meta:
    #     db_table = "GT004_map"
    #     verbose_name = "マップテーブル"





#緯度と経度をjsonデータ型で受け取る例
#{
#    "coordinates": {
#    "latitude": "40.7128",
#    "longitude": "-74.0060"
#    }
#}


