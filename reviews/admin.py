from django.contrib import admin
from reviews.models import Review
# Register your models here.


class ReviewAdmin(admin.ModelAdmin):

    list_display = ["id", "title", "content", "movie_code",]
    list_filter = ["title",]
    fieldsets = []

    search_fields = ["title", "content",]
    ordering = ["title"]
    filter_horizontal = []
    list_display_links = ["id", "title", "content", "movie_code",]


admin.site.register(Review, ReviewAdmin)
