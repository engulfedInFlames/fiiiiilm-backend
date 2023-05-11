from django.contrib import admin
from reviews.models import Review, Comment
# Register your models here.


class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "movie_code",
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
        "movie_code",
    ]


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "content",
    )


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
