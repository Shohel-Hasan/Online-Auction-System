from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('auctions/', views.all_auction, name='auctions'),
    path('create/', views.create, name='create'),
    path('bid/<int:id>/', views.bid, name='bid'),
    path('all-bids/<int:id>/', views.all_bids, name='all_bids'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('user-create/', views.CreateUser, name='user-create' ),
    path('profile/<str:user>/', views.profile, name='profile'),
    path('profile-edit/<str:user>/', views.profile_edit, name='profile-edit'),

]