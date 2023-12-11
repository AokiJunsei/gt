from django.contrib import admin
from .models import Account, SearchHistory, Spot, MapCar ,MapBike

#アカウントテーブル
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user','last_name','first_name','address','gender','zipcode','state','city','address_1','address_2',)
    search_fields = ('name', 'address')

#検索履歴テーブル
@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('history_id', 'account', 'search_datetime', 'search_query', 'start_location','end_location','travel_mode')
    search_fields = ('account.last_name', 'search_query')

#スポットテーブル
@admin.register(Spot)
class SpotAdmin(admin.ModelAdmin):
    list_display = ('spot_id', 'account', 'address', 'json_data_display')
    def json_data_display(self, obj):
        return obj.json_data
    json_data_display.short_description = 'JSON Data'

# マップ一覧
@admin.register(MapCar)
class MapCarAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'json_data_display')

    def json_data_display(self, obj):
        return obj.json_data
    json_data_display.short_description = 'JSON Data'

# マップ一覧
@admin.register(MapBike)
class MapBikeAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'json_data_display')

    def json_data_display(self, obj):
        return obj.json_data
    json_data_display.short_description = 'JSON Data'