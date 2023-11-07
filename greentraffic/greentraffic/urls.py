
from django.contrib import admin
from django.urls import path,include

from gt.views import top_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', top_page)
    
]
