from django.contrib import admin
from reviews.models import Review
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class ReviewAdmin(UserAdmin):

    list_display = ["id", "title", "content"]
    list_filter = ["title"]
    fieldsets = []

    search_fields = ["title"]
    ordering = ["title"]
    filter_horizontal = []
    list_display_links = ["id", "title", "content"]


admin.site.register(Review, ReviewAdmin)
