from django.urls import path
from .views import (
    AdvertisementList, AdvertisementDetail, AdvertisementResponses, MyAdvertisementList, AdvertisementCreate, AdvertisementUpdate,
    accept_response, remove_accepted_author, decline_response, like_author, dislike_author, state_change,

)


urlpatterns = [
    path('', AdvertisementList.as_view(), name='advertisements'),
    path('<int:pk>', AdvertisementDetail.as_view(), name='advertisement'),
    path('my/<int:pk>', AdvertisementDetail.as_view(), name='my_advertisement'),
    path('create/', AdvertisementCreate.as_view(), name='advertisement_create'),
    path('edit/<int:pk>/', AdvertisementUpdate.as_view(), name='advertisement_update'),
    path('<int:pk>/responses/', AdvertisementResponses.as_view(), name='responses'),
    path(r'accepted/(<pk>[0-9]+)(<response_pk>[-\w]+)/', accept_response, name='accept'),
    path(r'deleted/(<pk>[0-9]+)(<response_pk>[-\w]+)/', decline_response, name='delete'),
    path(r'removed/(<pk>[0-9]+)(<author_id>[-\w]+)/', remove_accepted_author, name='remove'),
    path(r'liked/(<pk>[0-9]+)(<author_id>[-\w]+)/', like_author, name='like'),
    path(r'disliked/(<pk>[0-9]+)(<author_id>[-\w]+)/', dislike_author, name='dislike'),
    path(r'state/(<pk>[0-9]+)/', state_change, name='state_change'),
    path('my/', MyAdvertisementList.as_view(), name='my-advertisements'),

]

