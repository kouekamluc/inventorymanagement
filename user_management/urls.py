from django.urls import path
from .views import UserProfileView, UserProfileUpdateView, CustomPasswordChangeView

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('profile/edit/', UserProfileUpdateView.as_view(), name='user_profile_edit'),
    path('password/change/', CustomPasswordChangeView.as_view(), name='custom_password_change'),

]