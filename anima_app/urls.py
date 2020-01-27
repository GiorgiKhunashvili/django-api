from django.urls import path
from .views import(
    api_detail_view,
    api_profile_update_view,
    api_profile_partial_update,
    registration_view,
    api_profile_delete_view,
    api_password_change_view,
    api_reset_password,
    api_reset_password_confirm
    )

from rest_framework.authtoken.views import obtain_auth_token

app_name = 'anima_app'

urlpatterns = [
    path('<username>/', api_detail_view, name="detail"),
    path("update/<username>", api_profile_update_view, name="update"),
    path("partial-update/<username>", api_profile_partial_update, name="partial_update"),
    path("delete/<username>", api_profile_delete_view, name="delete_user"),
    path('register', registration_view, name="register"),
    path('login', obtain_auth_token, name='login'),
    path('change-password', api_password_change_view, name='password_change'),
    path('reset-password', api_reset_password, name='password_reset'),
    path('reset-password-confirm', api_reset_password_confirm, name="password_reset_confirm"),

]
