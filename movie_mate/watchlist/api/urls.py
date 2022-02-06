from django.urls import path, include
from watchlist.api.views import (
    WatchListDetailView,
    WatchListView,
    StreamingPlatFormView,
    StreamingPlatformDetailView,
    ReviewList,
    ReviewDetail,
    ReviewCreate,
    StreamPlatformAV
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('stream', StreamPlatformAV, basename='stream-platform')
urlpatterns = [
    path('list/', WatchListView.as_view(), name='list'),
    path('<int:pk>', WatchListDetailView.as_view(), name="movie_detail"),
    path('platform/', StreamingPlatFormView.as_view(), name='platform'),
    path(
        "platform/<int:pk>",
        StreamingPlatformDetailView.as_view(),
        name='platform'
    ),
    path(
        'platform/<int:pk>/review-create',
        ReviewCreate.as_view(),
        name="review-create"
    ),
    path(
        'platform/<int:pk>/review/',
        ReviewList.as_view(),
        name="review-list"
    ),
    path(
        'platform/review-detail/<int:pk>',
        ReviewDetail.as_view(),
        name="review-detail"
    ),
    path('', include(router.urls)),
]
