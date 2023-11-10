
from django.contrib import admin
from django.urls import path,include

from gt.views import top_page
from gt.views import admin_map_register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', top_page),
    #テスト下用に↓
    path('map_register/', admin_map_register)
    
]
