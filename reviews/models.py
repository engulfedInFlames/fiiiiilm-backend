from django.db import models
# from users.models import User
from django.utils import timezone
# Create your models here.


class Review(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    # like_users = models.ManyToManyField(User,related_name=like_reviews,blank=True)
    title = models.CharField(max_length=255,)
    content = models.CharField(max_length=255,)
    created_at = models.DateTimeField(auto_now_add=True,)
    updated_at = models.DateTimeField(auto_now=True,)

    def __str__(self):
        return str(self.title)
