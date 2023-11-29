from django.contrib import admin
from .models import Account, SearchHistory, Spot, Map

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user','last_name','first_name','address','gender','zipcode','state','city','address_1','address_2',)
    search_fields = ('name', 'address')
    #アカウントテーブル

@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('history_id', 'account', 'search_result', 'search_datetime', 'search_query', 'search_type')
    search_fields = ('account__name', 'search_result', 'search_query')
    #検索履歴テーブル

@admin.register(Spot)
class SpotAdmin(admin.ModelAdmin):
    list_display = ('spot_id', 'spot_name', 'account', 'category', 'address', 'contact_info', 'fee_info', 'business_hours', 'latitude', 'longitude')
    search_fields = ('spot_name', 'account__name', 'category', 'address')
    #スポットテーブル

@admin.register(Map)
class MapAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'json_data_display')

    def json_data_display(self, obj):
        return obj.json_data
    json_data_display.short_description = 'JSON Data'
