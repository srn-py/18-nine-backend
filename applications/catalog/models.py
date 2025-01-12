import io
import os

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.utils.translation import gettext_lazy as _
from commons.abstract_models import DateTimeBasedModel


class Category(DateTimeBasedModel):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_('Category Name'),
        help_text=_('Name of the category (e.g., Mens wear, Women\'s wear ).')
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('Category Description'),
        help_text=_('A description of the category and its products.')
    )
    parent_category = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name=_('Parent Category'),
        help_text=_('The parent category for subcategories (if any).')
    )
    slug = models.SlugField(
        unique=True,
        verbose_name=_('Slug'),
        help_text=_('URL-friendly version of the category name.')
    )
    image = models.ImageField(
        upload_to='category_images/',
        null=True,
        blank=True,
        verbose_name=_('Category Image'),
        help_text=_('An image representing the category.')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Active'),
        help_text=_('Indicates whether the category is currently active.')
    )
    meta_title = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('Meta Title'),
        help_text=_('SEO title for the category page.')
    )
    meta_description = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('Meta Description'),
        help_text=_('SEO description for the category page.')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['name']


class Fabric(DateTimeBasedModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Fabric')
        verbose_name_plural = _('Fabrics')
        ordering = ['name']


class Color(DateTimeBasedModel):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(
        upload_to='color_images/',
        verbose_name=_('Image'),
        help_text=_('The image of the color')
    )
    hex_value = models.CharField(max_length=7, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Color')
        verbose_name_plural = _('Colors')
        ordering = ['name']

    def save(self, *args, **kwargs):
        # If the image exists, resize it
        if self.image:
            img = Image.open(self.image)
            img = img.convert(
                'RGB')  # Convert to RGB if it's in another mode (like RGBA)

            # Resize image to 50x50 pixels
            img = img.resize((50, 50),
                             Image.Resampling.LANCZOS)  # Use LANCZOS for high-quality resizing

            # Check if the original image is PNG or JPG and save accordingly
            file_extension = os.path.splitext(self.image.name)[1].lower()  # Get the file extension (e.g., .jpg or .png)

            # Create in-memory file for resized image
            image_io = io.BytesIO()

            if file_extension == 'png':
                img.save(image_io,
                         format='PNG')  # Save as PNG if original is PNG
                image_io.seek(0)
                self.image = InMemoryUploadedFile(
                    image_io, None, self.image.name, 'image/png',
                    image_io.tell(), None
                )
            else:
                img.save(image_io,
                         format='JPEG')  # Save as JPEG if original is JPG
                image_io.seek(0)
                self.image = InMemoryUploadedFile(
                    image_io, None, self.image.name, 'image/jpeg',
                    image_io.tell(), None
                )

        super(Color, self).save(*args, **kwargs)


class Pattern(DateTimeBasedModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Pattern')
        verbose_name_plural = _('Patterns')
        ordering = ['name']


class Shape(DateTimeBasedModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Neck(DateTimeBasedModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Length(DateTimeBasedModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class SleeveLength(DateTimeBasedModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Size(DateTimeBasedModel):
    name = models.CharField(max_length=20, unique=True)
    code = models.CharField(max_length=4, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Size')
        verbose_name_plural = _('Sizes')
        ordering = ['name']


class SizeAttribute(DateTimeBasedModel):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('Size Attribute Name'),
        help_text=_('Name of the size attribute (e.g., Waist, Shoulder, Hip).')
    )
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _('Size Attribute')
        verbose_name_plural = _('Size Attributes')
        ordering = ['name']
