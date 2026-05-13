from django.urls import path

from .views import (
    UserListView,
    UserDetailView,
    UserRegisterView,
    UserLoginView,
    UserEditView,
    CustomPasswordChangeView,
    CustomLogoutView,
)

app_name = "users"

urlpatterns = [
    path("list/", UserListView.as_view(), name="user_list"),
    path("<int:pk>/", UserDetailView.as_view(), name="user_detail"),

    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),

    path("edit/", UserEditView.as_view(), name="user_edit"),
    path("edit-profile/", UserEditView.as_view(), name="edit_profile"),

    path("password/", CustomPasswordChangeView.as_view(), name="password_change"),
    path("change-password/", CustomPasswordChangeView.as_view(), name="change_password"),
]