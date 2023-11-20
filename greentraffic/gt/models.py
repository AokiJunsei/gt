from django.db import models
from django.contrib.auth.models import User

# ユーザーアカウントのモデルクラス
class Account(models.Model):

    # ユーザー認証のインスタンス(1対1関係)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # 追加フィールド
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=7, blank=True)
    state = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=255, blank=True)
    address_1 = models.CharField(max_length=100, blank=True)
    address_2 = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=1, choices=[('M', '男'), ('F', '女'), ('O', 'その他')], blank=True)  # 性別

    def __str__(self):
        return self.user.username


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

    class Meta:
        db_table = "GT002_search_history"
        verbose_name = "検索履歴テーブル"


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
    coordinates = models.JSONField(verbose_name="座標", blank=True, null=True)

    def __str__(self):
        return f"{self.spot_id} - {self.spot_name}"

    class Meta:
        db_table = "GT003_spot"
        verbose_name = "スポットテーブル"


# マップテーブル
class Map(models.Model):
    map_id = models.AutoField(primary_key=True, verbose_name="マップID")
    location_name = models.CharField(max_length=100, verbose_name="位置名")
    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="アカウントID")
    category = models.CharField(max_length=100, verbose_name="カテゴリ")
    address = models.CharField(max_length=100, verbose_name="住所")
    coordinates = models.JSONField(verbose_name="座標", blank=True, null=True)
    
    def __str__(self):
        return f"{self.map_id} - {self.location_name}"
    
    class Meta:
        db_table = "GT004_map"
        verbose_name = "マップテーブル"





#緯度と経度をjsonデータ型で受け取る例
#{
#    "coordinates": {
#    "latitude": "40.7128",
#    "longitude": "-74.0060"
#    }
#}


