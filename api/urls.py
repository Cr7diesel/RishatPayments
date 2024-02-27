from django.urls import path

from .views import GetItemAPiView, GetSessionAPiView


urlpatterns = [
    path('buy/<str:id>/', GetSessionAPiView.as_view(), name='buy_item'),
    path('item/<int:id>/', GetItemAPiView.as_view(), name='get_item'),
]
