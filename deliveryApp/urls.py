from . import views
from django.urls import include, path


urlpatterns = [
    path('',views.index,name='index'),
    path('add_food_item',views.add_food_item,name="add_food_item"),
    path('item_desc/<pk>',views.item_desc,name="item_desc"),
    path('add_to_cart/<pk>',views.add_to_cart,name="add_to_cart"),
    path('orderlist',views.orderlist,name="orderlist"),
    path('add_item/<int:pk>',views.add_item,name="add_item"),
    path('remove_item/<int:pk>',views.remove_item,name="remove_item"),
    path('checkout',views.checkout,name="checkout"),
]
