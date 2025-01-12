from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _
from .models import Product, ProductVariant, SizeAttribute, UserReview, \
    ReviewImage, ProductVariantImage
from django.forms import TextInput, Textarea


# Inline classes for ProductVariant and SizeAttribute
class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = (
        'variant_name', 'colors', 'size', 'offer_percentage',
        'stock_count', 'sku', 'is_active'
    )
    readonly_fields = ('slug',)
    autocomplete_fields = ['colors', 'size']


class SizeAttributesInline(admin.TabularInline):
    model = SizeAttribute
    extra = 1
    fields = ('size', 'attribute', 'centimeter', 'inch')
    autocomplete_fields = ['size', 'attribute']


class ProductVariantImageInline(admin.TabularInline):
    model = ProductVariantImage
    extra = 1
    fields = ['image', 'is_primary']
    show_change_link = True
    max_num = 10

    def has_add_permission(self, request, obj=None):
        return obj.variant_images.count() < 10


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'base_price', 'overall_rating', 'exclusive',
        'quality_checked', 'return_policy', 'slug'
    )
    search_fields = ('name',)
    inlines = [ProductVariantInline]

    # Customizing form fields for some models
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'cols': 80, 'rows': 5})},
        models.CharField: {'widget': TextInput(attrs={'size': '80'})},
    }

    # Additional configuration for the admin interface
    fieldsets = (
        (None, {
            'fields': (
                'name', 'description', 'base_price', 'overall_rating',
                'exclusive', 'return_policy', 'exchange_policy',
                'pay_on_delivery', 'pattern', 'fabric', 'shape', 'neck',
                'length', 'sleeve_length', 'instructions', 'wash_care',
                'quality_checked', 'categories'
            )
        }),
    )

    def get_queryset(self, request):
        """
        Optimize the query to fetch related images with the product variants
        """
        return super().get_queryset(request).prefetch_related('variant_images')

    def save_model(self, request, obj, form, change):
        # Custom save logic if needed
        super().save_model(request, obj, form, change)


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = (
        'product', 'variant_name', 'size', 'offer_percentage',
        'stock_count', 'sku', 'get_base_price', 'get_offer_price',
        'is_active'
    )
    search_fields = ('sku', 'variant_name')
    autocomplete_fields = ['size']
    list_filter = ('product', 'colors', 'size', 'is_active')
    inlines = [ProductVariantImageInline, SizeAttributesInline]

    def get_offer_price(self, obj):
        return obj.get_offer_price()

    get_offer_price.admin_order_field = 'offer_price'
    get_offer_price.short_description = _('Offer Price')

    def get_base_price(self, obj):
        return obj.product.base_price

    get_base_price.admin_order_field = 'base_price'
    get_base_price.short_description = _('Base Price')


@admin.register(ProductVariantImage)
class ProductVariantImageAdmin(admin.ModelAdmin):
    list_display = ['variant', 'image', 'is_primary']
    list_filter = ['is_primary']
    search_fields = ['variant__product__name', 'variant__sku', 'image']
    actions = ['mark_as_primary', 'remove_images']

    def mark_as_primary(self, request, queryset):
        """Mark selected images as primary for the variant."""
        for image in queryset:
            image.variant.variant_images.update(
                is_primary=False)  # Reset any existing primary image
            image.is_primary = True
            image.save()

    def remove_images(self, request, queryset):
        """Remove selected images."""
        queryset.delete()

    mark_as_primary.short_description = "Mark selected images as primary"
    remove_images.short_description = "Delete selected images"

    def get_queryset(self, request):
        """Optimize the query to include the related ProductVariant."""
        return super().get_queryset(request).select_related('variant')


@admin.register(SizeAttribute)
class SizeAttributeAdmin(admin.ModelAdmin):
    list_display = ('size', 'product_variant', 'attribute', 'centimeter', 'inch')
    search_fields = ('size__name', 'product_variant__sku', 'attribute__name')
    list_filter = ('size', 'attribute')


@admin.register(UserReview)
class UserReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product_variant', 'rating', 'likes', 'dislikes', 'is_verified', 'created')
    search_fields = ('user__username', 'product_variant__sku', 'rating')
    list_filter = ('is_verified', 'rating', 'created')


@admin.register(ReviewImage)
class ReviewImageAdmin(admin.ModelAdmin):
    list_display = ('review', 'image', 'created')
    search_fields = ('review__id',)
