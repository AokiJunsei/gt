# from django.urls import path

# from . import views

# app_name = 'gt'
# urlpatterns = [
#     path('', views.top_page.as_view(), name="top"),
    
    
#     path('map_change/<int:pk>/', views.admin_map_change, name='admin_map_change'),
#     path('map_delete/<int:pk>/', views.admin_map_delete, name='admin_map_delete'),
#     path('map_register/', views.admin_map_register, name='admin_map_register'),
#     #利用者ページpath書く
#     path('map_detail/<int:pk>/', views.admin_map_detail, name='admin_map_detail'),
    
# ]

from django.urls import path
from . import views

app_name = 'gt'
urlpatterns = [
    path('', views.top_page, name="top"),
    path('map_change/<int:pk>/', views.admin_map_change, name='admin_map_change'),
    path('map_delete/<int:pk>/', views.admin_map_delete, name='admin_map_delete'),
    path('map_register/', views.admin_map_register, name='admin_map_register'),
    # path('map_detail/<int:pk>/', views.admin_map_detail, name='admin_map_detail'),
    # ここに利用者ページのpathを追加
]




