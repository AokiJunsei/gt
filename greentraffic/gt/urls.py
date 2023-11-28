from django.urls import path

from . import views

app_name = 'gt'
urlpatterns = [
    path('', views.top_page, name="top"),
    path('admin_top/', views.admin_top, name="admin_top"),
    
    path('map_change/<int:pk>/', views.admin_map_change, name='admin_map_change'),
    path('map_delete/<int:pk>/', views.admin_map_delete, name='admin_map_delete'),
    path('map_register/', views.admin_map_register, name='admin_map_register'),
    #利用者ページpath書く
    path('map_detail/<int:pk>/', views.admin_map_detail, name='admin_map_detail'),
    
    
    path('account_info/', views.user_info, name='user_info'),
    path('user_update/', views.user_update_view, name='user_update'),
    path('user_delete/', views.user_delete_view, name='user_delete'),
    
    
    
    path('account_history/', views.account_history_view, name='account_history'),
    path('log_detail/', views.log_detail_view, name='log_detail'),


    path('accounts/login/', views.Login, name='user_login'),
    path('logout/', views.Logout, name='logout'),
    path('register/', views.AccountRegistration.as_view(), name='register'),
    path('user_spot_addspot/', views.user_spot_addspot_view, name='user_spot_addspot'),
]





