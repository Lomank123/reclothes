import json
from datetime import timedelta

from accounts.models import CustomUser
from carts.models import Cart, CartItem
from catalogue.models import (ActivationKey, Category, OneTimeUrl, Product,
                              ProductAttribute, ProductAttributeValue,
                              ProductFile, ProductImage, ProductReview,
                              ProductType, Tag)
from django.contrib import auth
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.backends.db import SessionStore
from django.test import RequestFactory
from django.utils import timezone
from orders.models import Order, OrderItem, StatusTypes
from rest_framework.request import Request

"""
Factory methods for most models.
"""


VALID_CARD_CREDENTIALS = {
    'card': json.dumps({
        'name': 'Card Holder',
        'number': '1231231231231231',
        'code': '123',
        'expiry_date': '4/22',
    }),
}

INVALID_CARD_CREDENTIALS = {
    'card': json.dumps({
        'name': '',
        'number': '123213',
        'code': '12',
        'expiry_date': '15-22',
    }),
}


def create_session(user):
    """
    Create and return new session.

    User must be either User or AnonymousUser object.
    """
    session = SessionStore(None)
    session.clear()
    session.cycle_key()
    if user.is_authenticated:
        session[auth.SESSION_KEY] = user._meta.pk.value_to_string(user)
        session[auth.BACKEND_SESSION_KEY] = (
            'django.contrib.auth.backends.ModelBackend')
        session[auth.HASH_SESSION_KEY] = user.get_session_auth_hash()
    session.save()
    return session


def create_request(user=None, session=None):
    request = RequestFactory().request()
    request.user = user
    request.session = session
    return request


def create_post_request(path='/', data=dict()):
    return RequestFactory().post(path=path, data=data)


def create_get_request(path='/', **kwargs):
    return RequestFactory().get(path, **kwargs)


def create_rest_request(request=RequestFactory().request()):
    return Request(request=request)


def create_user(email=None, password='123123123Aa', **kwargs):
    """Create CustomUser or AnonymousUser based on provided email."""
    if email is None:
        return AnonymousUser()
    return CustomUser.objects.create(email=email, password=password, **kwargs)


def create_product_type(name):
    return ProductType.objects.create(name=name)


def create_image(product_id, alt_text='img', is_feature=False, **kwargs):
    return ProductImage.objects.create(
        product_id=product_id,
        alt_text=alt_text,
        is_feature=is_feature,
        **kwargs,
    )


def create_product_review(product_id, user_id, rating=5, text='t', **kwargs):
    return ProductReview.objects.create(
        product_id=product_id,
        user_id=user_id,
        rating=rating,
        text=text,
        **kwargs,
    )


def create_product_attr(name, type_id, **kwargs):
    return ProductAttribute.objects.create(
        name=name, product_type_id=type_id, **kwargs)


def create_product_attr_value(product_id, attr_id, value='1', **kwargs):
    return ProductAttributeValue.objects.create(
        product_id=product_id, attribute_id=attr_id, value=value, **kwargs)


def create_product(type_id, title='test', regular_price=100, **kwargs):
    return Product.objects.create(
        product_type_id=type_id,
        title=title,
        regular_price=regular_price,
        **kwargs,
    )


def create_activation_key(product_id, key, **kwargs):
    expiry_date = timezone.now() + timedelta(days=1)
    return ActivationKey.objects.create(
        product_id=product_id, key=key, expired_at=expiry_date, **kwargs)


def create_cart(user_id=None, **kwargs):
    return Cart.objects.create(user_id=user_id, **kwargs)


def create_order(user, **kwargs):
    return Order.objects.create(
        user=user,
        status=StatusTypes.IN_PROGRESS.value,
        total_price=123,
        **kwargs,
    )


def create_order_item(order_id, cart_item_id):
    return OrderItem.objects.create(
        order_id=order_id, cart_item_id=cart_item_id)


def create_cart_item(cart_id, product_id, **kwargs):
    return CartItem.objects.create(
        cart_id=cart_id, product_id=product_id, **kwargs)


def create_tag(**kwargs):
    return Tag.objects.create(**kwargs)


def create_category(**kwargs):
    return Category.objects.create(**kwargs)


def create_one_time_url(**kwargs):
    return OneTimeUrl.objects.create(**kwargs)


def create_product_file(**kwargs):
    return ProductFile.objects.create(**kwargs)
