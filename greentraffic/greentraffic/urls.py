
from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('gt/', include('gt.urls', namespace='gt')),

]
