from django.apps import AppConfig
from django.utils import timezone
import datetime

class GtConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gt'

    def ready(self):
        from django.db.models import F
        from .models import SearchHistory

        # 1週間前の日時を計算
        one_week_ago = timezone.now() - datetime.timedelta(weeks=1)

        # 条件に合致するレコードを削除
        SearchHistory.objects.filter(search_datetime__lt=one_week_ago).delete()