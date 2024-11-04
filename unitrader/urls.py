from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('logout/', views.custom_logout, name='logout'),  
    path('sell/', views.sell_item, name='sell_item'),  
    path('buy/', views.buy_items, name='buy_items'), 
    path('buy/confirm/<int:item_id>/', views.buy_now, name='buy_now'), 
    path('bid/<int:item_id>/', views.bid_on_item, name='bid_on_item'),
    path('chat/seller/<int:seller_id>/', views.chat_with_seller, name='chat_with_seller'),
    path('inbox/', views.inbox, name='inbox'),
    path('confirm-purchase/<int:item_id>/', views.confirm_purchase, name='confirm_purchase'),
    #path('bid/<int:item_id>/', views.bid_on_item, name='bid_on_item'),
    path('finalize-auctions/', views.finalize_auctions, name='finalize_auctions')
]
