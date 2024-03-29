from django.urls import path
from .views import activate_account  # 必要に応じてビューをインポート
from . import views

app_name = 'gt'
urlpatterns = [
    path('', views.top_page, name="top"),# 車
    path('admin_top/', views.admin_top, name="admin_top"),

    path('search_bike/', views.user_search_bike, name="search_bike"),
    path('search_walk/', views.user_search_walk, name="search_walk"),
    path('search_short/', views.user_search_short, name="search_short"),
    path('search_cheap/', views.user_search_cheap, name="search_cheap"),
    path('search_share_car_car/', views.user_search_share_car_car, name="search_share_car_car"),
    path('search_share_car_bike/', views.user_search_share_car_bike, name="search_share_car_bike"),
    path('search_share_car_walk/', views.user_search_share_car_walk, name="search_share_car_walk"),
    path('search_share_bike_car/', views.user_search_share_bike_car, name="search_share_bike_car"),
    path('search_share_bike_bike/', views.user_search_share_bike_bike, name="search_share_bike_bike"),
    path('search_share_bike_walk/', views.user_search_share_bike_walk, name="search_share_bike_walk"),
    path('my_map/', views.user_my_map, name="my_map"),
    path('my_map_shop/',views.user_my_map_shop, name="my_map_shop"),

    path('map_change/<str:vehicle_type>/<int:pk>/', views.admin_map_change, name='admin_map_change'),
    path('map_delete/<str:vehicle_type>/<int:pk>/', views.admin_map_delete, name='admin_map_delete'),
    path('map_register/', views.admin_map_register, name='admin_map_register'),
    path('map_detail/<str:vehicle_type>/<int:pk>/', views.admin_map_detail, name='admin_map_detail'),
    path('admin_user_info/', views.admin_user_info, name="admin_user_info"),

    path('account_info/', views.user_info, name='user_info'),
    path('user_update/', views.user_update_view, name='user_update'),
    path('user_delete/', views.user_delete_view, name='user_delete'),

    path('account_history/', views.account_history_view, name='account_history'),
    path('log_detail/<int:pk>/', views.log_detail_view, name='log_detail'),
    path('log_delete/<int:pk>/', views.log_delete_view, name='log_delete'),

    path('accounts/login/', views.Login, name='user_login'),
    path('logout/', views.Logout, name='logout'),
    path('register/', views.AccountRegistration.as_view(), name='register'),
    path('activate/<str:username>/<str:token>/', activate_account, name='activate'),
    path('registration_complete/', views.registration_complete, name='registration_complete'),

    path('spot_list/', views.user_spot_list, name='user_spot_list'),
    path('spot_change/<int:pk>/', views.user_spot_change, name='user_spot_change'),
    path('spot_delete/<int:pk>/', views.user_spot_delete, name='user_spot_delete'),
    path('spot_detail/<int:pk>/', views.user_spot_detail, name='user_spot_detail'),
    path('spot_register/', views.user_spot_register, name='user_spot_register'),


    path('api/user_accounts/', views.get_accounts, name='get_accounts'),
    path('api/user_histories', views.get_search_histories, name='get_search_histories'),
    path('api/user_spots', views.get_spots, name='get_spots'),
    path('api/map_cars', views.get_map_cars, name='get_map_cars'),
    path('api/map_bikes', views.get_map_bikes, name='get_map_bikes'),

    path('fetch_jorudan_cheap_route/', views.fetch_jorudan_cheap_route, name='fetch_jorudan_cheap_route')
    ]