from django.contrib import admin
from .models import Category, Fabric, Color, Pattern, Size, SizeAttribute, Shape, \
    Length, Neck, SleeveLength


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_category', 'is_active', 'created', 'modified')
    list_filter = ('is_active', 'parent_category')
    search_fields = ('name', 'description', 'meta_title', 'meta_description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Fabric)
class FabricAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'modified')
    search_fields = ('name', 'description')


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'hex_value', 'image', 'created', 'modified')
    search_fields = ('name', 'hex_value')


@admin.register(Pattern)
class PatternAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'modified')
    search_fields = ('name', 'description')


@admin.register(Shape)
class ShapeAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'modified')
    search_fields = ('name', 'description')


@admin.register(Length)
class LengthAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'modified')
    search_fields = ('name', 'description')


@admin.register(Neck)
class NeckAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'modified')
    search_fields = ('name', 'description')


@admin.register(SleeveLength)
class SleeveLengthAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'modified')
    search_fields = ('name', 'description')


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'created', 'modified')
    search_fields = ('name', 'code')


@admin.register(SizeAttribute)
class SizeAttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'modified')
    search_fields = ('name',)
