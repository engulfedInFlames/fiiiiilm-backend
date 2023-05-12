from django.db import models
from django.urls import reverse
from users.models import User


class Review(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    like_users = models.ManyToManyField(
        User,
        related_name="like_reviews",
    )
    movie_code = models.IntegerField(null=True, blank=True)
    movie_title = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    title = models.CharField(
        max_length=255,
    )
    content = models.CharField(
        max_length=1000,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("review_detail", kwargs={"pk": self.pk})


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.CharField(
        max_length=225,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.content)
