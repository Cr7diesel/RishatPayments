from django.urls import path

from . import views


urlpatterns = [
    path('buy/<int:id>/', views.GetSessionAPiView.as_view(), name='buy_item'),
    path('item/<int:id>/', views.GetItemAPiView.as_view(), name='get_item'),
    path('createitem/', views.CreateItemView.as_view(), name='create_item'),
    path('getallitems/', views.GetAllItemView.as_view(), name='get_all_item'),
    path('getoneitem/<int:id>/', views.GetItemView.as_view(), name='get_one_item'),
    path('updateitem/<int:id>/', views.UpdateItemView.as_view(), name='update_item'),
    path('deleteitem/<int:id>/', views.DeleteItemView.as_view(), name='delete_item'),
    path('createorder/', views.CreateOrderView.as_view(), name='create_order'),
    path('getallorders/', views.GetAllOrdersApiView.as_view(), name='get_all_orders'),
    path('getoneorder/<int:id>/', views.GetOrderView.as_view(), name='get_one_order'),
    path('updateorder/<int:id>/', views.UpdateOrderView.as_view(), name='update_order'),
    path('deleteorder/<int:id>/', views.DeleteOrderView.as_view(), name='delete_order'),
]
