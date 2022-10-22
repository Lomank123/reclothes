from django.urls import path

from payment import views


card_api = ([
    path('', views.CardAPIView.as_view(), name='card-validation'),
], 'card')


urlpatterns = []
