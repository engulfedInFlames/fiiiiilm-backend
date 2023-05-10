from django.urls import path
from reviews import views

urlpatterns = [
    path('api/v1/movie', views.MovieApiMain.as_view(), name='main_api'),# 영화api 임시
    path('api/v1/movie/detail', views.MovieApiDetail.as_view(), name='detail_api'),# 영화api 임시
    path('api/v1/reviews', views.ReviewList.as_view(), name='review_list'),
    path('api/v1/reviews/recent',views.ReviewListRecent.as_view(), name='review_recent'),
    path('api/v1/reviews/<int:pk>',views.ReviewListDetail.as_view(), name='review_detail'),
    path('/api/v1/reviews/<int:pk>/comments',views.CommentList.as_view(), name='comment_list'),
    path('/api/v1/comments/<int:pk>/',views.CommentDetail.as_view(), name='comment_detail'),
]
