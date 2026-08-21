from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

from .models import (
    Product,
    Category,
    Cart,
    CartItem,
    Wishlist,
    Order,
    OrderItem
)


def home(request):

    products = Product.objects.all().order_by("-created_at")[:8]
    categories = Category.objects.all()

    return render(
        request,
        "store/home.html",
        {
            "products": products,
            "categories": categories
        }
    )


def products(request):

    product_list = Product.objects.all()
    categories = Category.objects.all()

    search = request.GET.get("search")
    category = request.GET.get("category")

    if search:
        product_list = product_list.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )

    if category:
        product_list = product_list.filter(
            category_id=category
        )

    return render(
        request,
        "store/products.html",
        {
            "products": product_list,
            "categories": categories
        }
    )


def product_detail(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )

    return render(
        request,
        "store/product_detail.html",
        {
            "product": product
        }
    )


# ---------------- LOGIN ----------------

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("home")

        return render(
            request,
            "store/login.html",
            {
                "error": "Invalid username or password"
            }
        )

    return render(
        request,
        "store/login.html"
    )


# ---------------- REGISTER ----------------

def register(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(
            username=username
        ).exists():

            return render(
                request,
                "store/register.html",
                {
                    "error": "Username already exists"
                }
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)

        return redirect("home")

    return render(
        request,
        "store/register.html"
    )


# ---------------- LOGOUT ----------------

@login_required
def logout_view(request):

    logout(request)

    return redirect("home")


# ---------------- CART ----------------

@login_required
def add_to_cart(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:

        item.quantity += 1
        item.save()

    return redirect("cart")


@login_required
def cart(request):

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    items = cart.items.all()

    total = sum(
        item.total_price()
        for item in items
    )

    return render(
        request,
        "store/cart.html",
        {
            "items": items,
            "total": total
        }
    )


@login_required
def remove_from_cart(request, id):

    item = get_object_or_404(
        CartItem,
        id=id,
        cart__user=request.user
    )

    item.delete()

    return redirect("cart")


# ---------------- WISHLIST ----------------

@login_required
def add_wishlist(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    return redirect("wishlist")


@login_required
def wishlist(request):

    items = Wishlist.objects.filter(
        user=request.user
    )

    return render(
        request,
        "store/wishlist.html",
        {
            "items": items
        }
    )


@login_required
def remove_wishlist(request, id):

    item = get_object_or_404(
        Wishlist,
        id=id,
        user=request.user
    )

    item.delete()

    return redirect("wishlist")


# ---------------- CHECKOUT ----------------

@login_required
def checkout(request):

    cart = get_object_or_404(
        Cart,
        user=request.user
    )

    items = cart.items.all()

    if not items.exists():

        return redirect("products")

    total = sum(
        item.total_price()
        for item in items
    )

    if request.method == "POST":

        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        order = Order.objects.create(
            user=request.user,
            name=name,
            phone=phone,
            address=address,
            total_amount=total
        )

        for item in items:

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

            item.product.stock -= item.quantity
            item.product.save()

        items.delete()

        return render(
            request,
            "store/order_success.html",
            {
                "order": order
            }
        )

    return render(
        request,
        "store/checkout.html",
        {
            "items": items,
            "total": total
        }
    )


# ---------------- ORDERS ----------------

@login_required
def orders(request):

    order_list = Order.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "store/orders.html",
        {
            "orders": order_list
        }
    )