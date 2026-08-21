from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "products/",
        views.products,
        name="products"
    ),

    path(
        "product/<int:id>/",
        views.product_detail,
        name="product_detail"
    ),

    path(
        "login/",
        views.login_view,
        name="login"
    ),

    path(
        "register/",
        views.register,
        name="register"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

    path(
        "cart/",
        views.cart,
        name="cart"
    ),

    path(
        "cart/add/<int:id>/",
        views.add_to_cart,
        name="add_to_cart"
    ),

    path(
        "cart/remove/<int:id>/",
        views.remove_from_cart,
        name="remove_from_cart"
    ),

    path(
        "wishlist/",
        views.wishlist,
        name="wishlist"
    ),

    path(
        "wishlist/add/<int:id>/",
        views.add_wishlist,
        name="add_wishlist"
    ),

    path(
        "wishlist/remove/<int:id>/",
        views.remove_wishlist,
        name="remove_wishlist"
    ),

    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),

    path(
        "orders/",
        views.orders,
        name="orders"
    ),
]