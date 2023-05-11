from django.urls import path, include
from users import views
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

urlpatterns = [
    path("signup/", views.UserView.as_view(), name="user_view"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("<int:user_id>/", views.UserDetailView.as_view(), name="user_detail_view"),
    path("<int:user_id>/follow/", views.FollowView.as_view(), name="follow_view"),
]
