from django.urls import path, re_path

from orders import views


order_api = ([
    path('', views.OrderListAPIView.as_view(), name='order-list'),
    path(
        '<int:pk>/',
        views.OrderDetailAPIView.as_view(),
        name='order-detail',
    ),
], 'order')


urlpatterns = [
    path('', views.OrderView.as_view(), name='order'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='my-order-detail'),
    path('my-orders/', views.MyOrdersView.as_view(), name='my-orders'),
    re_path(
        r'^download/(?P<url_token>\w+)/$',
        views.DownloadFileView.as_view(),
        name='download',
    ),
]
