from django.contrib import admin
from .models import Category, Article, ReadingHistory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "color"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "source_name", "category", "is_trending", "is_breaking", "published_at"]
    list_filter = ["category", "is_trending", "is_breaking", "source_name"]
    search_fields = ["title", "content"]
    prepopulated_fields = {"slug": ("title",)}


@admin.register(ReadingHistory)
class ReadingHistoryAdmin(admin.ModelAdmin):
    list_display = ["user", "article", "read_at", "completed"]
