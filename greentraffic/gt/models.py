from django.db import models
from django.contrib.auth.models import User
# アカウントテーブル
class Account(models.Model):
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
    gender = models.CharField(max_length=100, choices=[('M', '男'), ('F', '女'), ('O', 'その他')], blank=True)  # 性別
    email_verified = models.CharField(max_length=100, blank=True, default='')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.user.username

# 検索履歴テーブル
class SearchHistory(models.Model):
    history_id = models.AutoField(primary_key=True, verbose_name="履歴ID")
    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="アカウントID")
    search_datetime = models.DateTimeField(auto_now_add=True, verbose_name="検索日時")
    search_query = models.CharField(max_length=100, verbose_name="検索クエリ")
    start_location = models.CharField(max_length=255, blank=True, null=True, verbose_name="出発地")
    end_location = models.CharField(max_length=255, blank=True, null=True, verbose_name="目的地")
    start_spot_label = models.CharField(max_length=255, blank=True, null=True, verbose_name="出発地スポット")
    end_spot_label = models.CharField(max_length=255, blank=True, null=True, verbose_name="目的地スポット")

    travel_mode = models.CharField(max_length=100, blank=True, null=True, verbose_name="トラベルモード")

    def __str__(self):
        return f"{self.history_id} - {self.account.last_name} - {self.search_query}"

# スポットテーブル
class Spot(models.Model):
    spot_id = models.AutoField(primary_key=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    spot_name = models.CharField(max_length=100,blank=True)
    address = models.CharField(max_length=100,blank=True)
    json_data = models.TextField(blank=True)

    def __str__(self):
        return f"{self.spot_id} - {self.spot_name}"

# マップテーブル(車)
class MapCar(models.Model):
    map_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,blank=True)
    address = models.CharField(max_length=200,blank=True)
    json_data = models.TextField(blank=True)

    def __str__(self):
        return self.name

# マップテーブル（自転車）
class MapBike(models.Model):
    map_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,blank=True)
    address = models.CharField(max_length=200,blank=True)
    json_data = models.TextField(blank=True)

    def __str__(self):
        return self.name