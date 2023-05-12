from django.urls import path, include
from users import views

urlpatterns = [
    path('', views.UserList.as_view(), name='user_list'),
    path('signup/', views.UserView.as_view(), name='user_view'),
    path("me/", views.Me.as_view()),
    path("<int:user_id>/", views.UserDetailView.as_view(), name="user_detail_view"),
    path("<int:user_id>/follow/", views.FollowView.as_view(), name="follow_view"),
    path("token/", views.CustomTokenObtainPairView.as_view(),
         name="token_obtain_pair"),
    # path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("kakao-login/", views.KaKaoLogin.as_view()),
    path("github-login/", views.GithubLogin.as_view()),
]
