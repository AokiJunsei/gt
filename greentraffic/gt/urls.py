from django.urls import path

from . import views

app_name = 'gt'
urlpatterns = [
    path('', views.top_page, name="top"),
    path('admin_top/', views.admin_top, name="admin_top"),
    
    path('search_cheap', views.user_search_cheap, name="search_cheap"),
    path('search_share_car', views.user_search_share_car, name="search_share_car"),
    path('search_share_bike', views.user_search_share_bike, name="search_share_bike"),
    path('my_map', views.user_my_map, name="my_map"),
    
    path('map_change/<str:vehicle_type>/<int:pk>/', views.admin_map_change, name='admin_map_change'),
    path('map_delete/<str:vehicle_type>/<int:pk>/', views.admin_map_delete, name='admin_map_delete'),
    path('map_register/', views.admin_map_register, name='admin_map_register'),
    path('map_detail/<str:vehicle_type>/<int:pk>/', views.admin_map_detail, name='admin_map_detail'),
    path('admin_user_info/', views.admin_user_info, name="admin_user_info"),
    
    path('account_info/', views.user_info, name='user_info'),
    path('user_update/', views.user_update_view, name='user_update'),
    path('user_delete/', views.user_delete_view, name='user_delete'),
    
    path('account_history/', views.account_history_view, name='account_history'),
    path('log_detail/', views.log_detail_view, name='log_detail'),
    path('accounts/login/', views.Login, name='user_login'),

    path('accounts/login/', views.Login, name='user_login'),
    path('logout/', views.Logout, name='logout'),
    path('register/', views.AccountRegistration.as_view(), name='register'),
]





