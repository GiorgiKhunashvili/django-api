from django.urls import path
from .views import api_detail_view, api_profile_update_view, api_profile_partial_update, registration_view
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'anima_app'

urlpatterns = [
    path('<username>/', api_detail_view, name="detail"),
    path("update/<username>", api_profile_update_view, name="update"),
    path("partial-update/<username>", api_profile_partial_update, name="partial_update"),
    path('register', registration_view, name="register"),
    path('login', obtain_auth_token, name='login'),
]
