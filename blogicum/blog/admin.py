from django.contrib import admin

from .models import Category, Location, Post


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'pub_date',
        'author',
        'category',
        'location',
        'is_published',
        'image',
    )
    list_editable = (
        'is_published',
        'pub_date',
        'category',
    )
    search_fields = (
        'title',
    )
    list_filter = ('category',)
    list_display_links = ('title',)


class PostInline(admin.StackedInline):
    model = Post
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )
    list_display = (
        'title',
    )


class LocationAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )
    list_display = (
        'name',
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
