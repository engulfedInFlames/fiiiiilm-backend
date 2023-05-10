from django.urls import path, include
from users import views
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

urlpatterns = [
    path('signup/', views.UserView.as_view(), name='user_view'),
    path('token/', TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('<int:user_id>/', views.UserDetail.as_view(), name='user_detail_view'),
    path('<int:user_id>/follow/', views.ToggleUserFollow.as_view(), name='follow_view'),
    path('', views.UserList.as_view(), name='user_list_view'),
    path('me/', views.Me.as_view(), name='me_detail_view'),
]