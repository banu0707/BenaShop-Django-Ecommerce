from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Category,
    Product,
    Cart,
    CartItem,
    Wishlist,
    Order,
    OrderItem
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "category_image",
    )

    def category_image(self, obj):

        if obj.image:
            return format_html(
                '<img src="{}" width="80" height="80" '
                'style="object-fit: cover; border-radius: 8px;">',
                obj.image.url
            )

        return "No Image"

    category_image.short_description = "Category Image"


admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Wishlist)
admin.site.register(Order)
admin.site.register(OrderItem)