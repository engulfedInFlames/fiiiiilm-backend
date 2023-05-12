from django.urls import path
from reviews import views

urlpatterns = [
    path("movie/", views.MovieApiMain.as_view(), name="main_api"),
    path("movie/<int:movie_code>/", views.MovieApiDetail.as_view(), name="detail_api"),
    path(
        "movie/<int:movie_code>/reviews/",
        views.ReviewList.as_view(),
        name="review_list",
    ),
    path("reviews/recent/", views.ReviewRecent.as_view(), name="review_recent"),
    path("reviews/<int:pk>/", views.ReviewDetail.as_view(), name="review_detail"),
    path("reviews/<int:pk>/like/", views.ReviewLike.as_view(), name="review_like"),
    path(
        "reviews/<int:pk>/comments/", views.CommentList.as_view(), name="comment_list"
    ),
    path("comments/<int:pk>/", views.CommentDetail.as_view(), name="comment_detail"),
]
