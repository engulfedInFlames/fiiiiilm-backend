from django.contrib import admin
from reviews.models import Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
    ]
    list_filter = [
        "title",
    ]
    search_fields = [
        "title",
        "content",
    ]
    ordering = ["title"]
    filter_horizontal = []
    list_display_links = [
        "id",
        "title",
    ]


admin.site.register(Review, ReviewAdmin)
