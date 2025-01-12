from decimal import Decimal

from autoslug import AutoSlugField
from autoslug.settings import slugify
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from commons.abstract_models import DateTimeBasedModel


class Product(DateTimeBasedModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_('Product Name'),
        help_text=_('The name of the product.')
    )
    description = models.TextField(
        verbose_name=_('Description'),
        help_text=_('A detailed description of the product.')
    )
    base_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        verbose_name=_("Base Price"),
        help_text=_(
            "Base price of the product if there are no variants or as a fallback."
        )
    )
    overall_rating = models.DecimalField(
        max_digits=3, decimal_places=2, default=0,
        verbose_name=_('Overall Rating'),
        help_text=_('The overall rating of the product based on user reviews.')
    )
    exclusive = models.BooleanField(
        default=False,
        verbose_name=_('Exclusive'),
        help_text=_('Indicates if the product is exclusive or not.')
    )
    return_policy = models.CharField(
        max_length=255,
        verbose_name=_('Return Policy'),
        help_text=_(
            'Return policy for the product '
            '(e.g., number of days, exchange only).'
        )
    )
    exchange_policy = models.CharField(
        max_length=255,
        verbose_name=_('Exchange Policy'),
        help_text=_('Exchange policy for the product (e.g., exchange only).')
    )
    pay_on_delivery = models.BooleanField(
        default=False,
        verbose_name=_('Pay on Delivery'),
        help_text=_('Whether this product allows cash on delivery.')
    )
    pattern = models.ForeignKey(
        'catalog.Pattern', related_name="products", on_delete=models.PROTECT,
        verbose_name=_("Pattern"),
        help_text=_("The pattern common to this product.")
    )
    fabric = models.ForeignKey(
        'catalog.Fabric', related_name='products', on_delete=models.PROTECT,
        verbose_name=_("Fabric"),
        help_text=_("The fabric used for the product.")
    )
    shape = models.ForeignKey(
        'catalog.Shape', related_name="products", on_delete=models.PROTECT,
        verbose_name=_("Shape"),
        help_text=_("The shape of the product.")
    )
    length = models.ForeignKey(
        'catalog.Length', related_name="products", on_delete=models.PROTECT,
        verbose_name=_("Length"),
        help_text=_("The length of the product.")
    )
    neck = models.ForeignKey(
        'catalog.Neck', related_name="products", on_delete=models.PROTECT,
        verbose_name=_("Neck"),
        help_text=_("The neck type of the product.")
    )
    sleeve_length = models.ForeignKey(
        'catalog.SleeveLength', related_name="products", on_delete=models.PROTECT,
        verbose_name=_("Sleeve Length"),
        help_text=_("The sleeve length of the product.")
    )
    instructions = models.TextField(
        null=True, blank=True,
        verbose_name=_('Instructions'),
        help_text=_('Instructions for use or any special guidelines.')
    )
    wash_care = models.TextField(
        null=True, blank=True,
        verbose_name=_('Wash Care Instructions'),
        help_text=_(
            'Instructions on wash care for the product.')
    )
    quality_checked = models.BooleanField(
        default=False,
        verbose_name=_('Quality Checked'),
        help_text=_('Indicates whether the product has been quality checked.')
    )
    slug = AutoSlugField(
        unique=True,
        populate_from='name',
        blank=True,
        null=True,
        verbose_name=_('Slug'),
        help_text=_('URL-friendly version of the product name.')
    )
    categories = models.ManyToManyField(
        'catalog.Category',
        verbose_name=_('Categories'),
        help_text=_('Categories that this product belongs to.')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ['name']


class ProductVariant(DateTimeBasedModel):
    product = models.ForeignKey(
        'Product', related_name='variants', on_delete=models.CASCADE,
        verbose_name=_('Product'),
        help_text=_('The product this variant belongs to.')
    )
    variant_name = models.CharField(
        max_length=100, unique=True,
        verbose_name=_('Variant Name'),
        help_text=_('Variant Name for the product')
    )
    colors = models.ManyToManyField(
        'catalog.Color', related_name='variants',
        blank=True,  # Allow variants to not have any colors
        verbose_name=_('Colors'),
        help_text=_('The colors available for this product variant.')
    )
    size = models.ForeignKey(
        'catalog.Size', related_name='variants', on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Size'),
        help_text=_('The size of this variant.')
    )
    offer_percentage = models.IntegerField(
        default=0.0,
        validators=[MinValueValidator(0), MaxValueValidator(99)],
        verbose_name=_("Offer Percentage"),
        help_text=_("Discount percentage applied to this variant (0-100).")
    )
    stock_count = models.IntegerField(
        verbose_name=_('Stock Count'),
        help_text=_('The number of units available for this variant.')
    )
    sku = models.CharField(
        max_length=100, unique=True,
        verbose_name=_('SKU'),
        help_text=_('Unique identifier for this product variant.')
    )
    slug = AutoSlugField(
        unique=True,
        populate_from='product__name',
        # You can adjust this if you want different logic for slug creation
        blank=True,
        null=True,
        verbose_name=_('Slug'),
        help_text=_('URL-friendly version of the product variant.')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Is Active'),
        help_text=_(
            'Indicates if this variant is active and available for sale.')
    )

    @property
    def get_offer_price(self):
        """
        Calculate the offer price for this variant.

        - Base price comes from the related product.
        - Adjusted by the offer percentage.
        """
        base_price = self.product.base_price

        # Convert the offer percentage to Decimal and calculate the discount amount
        offer_percentage = Decimal(self.offer_percentage)

        # Calculate the final price with the discount applied
        final_price = (Decimal(100) - offer_percentage) / Decimal(
            100) * base_price

        return final_price

    def __str__(self):
        return f"{self.variant_name} - {self.size}"

    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate the slug based on product name, and size
            slug_string = f"{self.variant_name}" \
                          f"{' - ' + self.size.name if self.size else ''}"
            self.slug = slugify(slug_string)
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'variant_name', 'size'],
                name='unique_product_variant_name_size'
            )
        ]
        verbose_name = _("Product Variant")
        verbose_name_plural = _("Product Variants")
        ordering = ['product__name', 'size']


class ProductVariantImage(DateTimeBasedModel):
    variant = models.ForeignKey(
        'ProductVariant', related_name='variant_images',
        on_delete=models.CASCADE,
        verbose_name=_('Product Variant'),
        help_text=_('The product variant this image belongs to.')
    )
    image = models.ImageField(
        upload_to='product_variant_images/',
        verbose_name=_('Image'),
        help_text=_('The image of the product variant.')
    )
    is_primary = models.BooleanField(
        default=False,
        verbose_name=_('Primary Image'),
        help_text=_(
            'Indicates if this is the primary image for the product variant.')
    )

    class Meta:
        verbose_name = _("Product Variant Image")
        verbose_name_plural = _("Product Variant Images")
        ordering = ['created']

    def __str__(self):
        return f"Image for {self.variant} - Primary: {self.is_primary}"


class SizeAttribute(DateTimeBasedModel):
    size = models.ForeignKey(
        'catalog.Size', related_name='attributes', on_delete=models.CASCADE,
        verbose_name=_('Size'),
        help_text=_('The size this attribute is associated with.')
    )
    product_variant = models.ForeignKey(
        'ProductVariant', related_name='size_attributes', on_delete=models.CASCADE,
        verbose_name=_('Product Variant'),
        help_text=_('The product variant this size attribute belongs to.')
    )
    attribute = models.ForeignKey(
        'catalog.SizeAttribute', related_name='size_values',
        on_delete=models.CASCADE,
        verbose_name=_('Size Attribute'),
        help_text=_('The specific attribute for this size (e.g., Waist, Hip).')
    )
    centimeter = models.FloatField(
        verbose_name=_('Centimeter'),
        help_text=_('The value of the attribute for this size in cm.')
    )
    inch = models.CharField(
        max_length=20,
        verbose_name=_('Unit'),
        help_text=_('The value of the attribute for this size in inch.')
    )

    def __str__(self):
        return f"{self.product_variant} - {self.size.name} - {self.attribute.name}"

    class Meta:
        verbose_name = _("Product Size Attribute")
        verbose_name_plural = _("Product Size Attributes")
        ordering = ['product_variant', 'size', 'attribute']


class UserReview(DateTimeBasedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='reviews', on_delete=models.CASCADE,
        verbose_name=_('User'),
        help_text=_('The user who submitted the review.')
    )
    product_variant = models.ForeignKey(
        'ProductVariant', related_name='reviews', on_delete=models.CASCADE,
        verbose_name=_('Product Variant'),
        help_text=_(
            'The specific variant of the product '
            'this review is associated with.')
    )
    rating = models.PositiveSmallIntegerField(
        verbose_name=_('Rating'),
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text=_('The rating given by the user (1-5).')
    )
    review_text = models.TextField(
        null=True, blank=True,
        verbose_name=_('Review Text'),
        help_text=_('The text content of the review.')
    )
    likes = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Likes'),
        help_text=_('The number of users who liked this review.')
    )
    dislikes = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Dislikes'),
        help_text=_('The number of users who disliked this review.')
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name=_('Is Verified Purchase'),
        help_text=_('Indicates whether the review is from a verified purchase.')
    )

    def __str__(self):
        return f"Review by {self.user} for " \
               f"{self.product_variant} ({self.rating}/5)"

    class Meta:
        verbose_name = _("User Review")
        verbose_name_plural = _("User Reviews")
        ordering = ['-created']


class ReviewImage(DateTimeBasedModel):
    review = models.ForeignKey(
        'UserReview', related_name='images', on_delete=models.CASCADE,
        verbose_name=_('Review'),
        help_text=_('The review to which this image belongs.')
    )
    image = models.ImageField(
        upload_to='review_images/',
        verbose_name=_('Image'),
        help_text=_('The image uploaded for this review.')
    )

    def __str__(self):
        return f"Image for Review {self.review.id} by {self.review.user}"

    class Meta:
        verbose_name = _("Review Image")
        verbose_name_plural = _("Review Images")
        ordering = ['-created']
