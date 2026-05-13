from django.urls import path

from .views import (
    UserListView, UserDetailView, UserRegisterView, UserLoginView,
    UserEditView, CustomPasswordChangeView, CustomLogoutView
)

urlpatterns = [
    path('list/', UserListView.as_view(), name='user_list'),
    path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('edit/', UserEditView.as_view(), name='user_edit'),
    path('password/', CustomPasswordChangeView.as_view(), name='password_change'),
]