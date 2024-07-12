from django.urls import path
from .views import (
    ProfileDetail, ProfileAuthorEdit

)


urlpatterns = [
    path('<int:pk>/', ProfileDetail.as_view(), name='profile'),
    path('<int:pk>/edit', ProfileAuthorEdit.as_view(), name='edit_profile'),

]

