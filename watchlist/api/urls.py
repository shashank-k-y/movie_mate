from django.urls import path, include

from rest_framework.routers import DefaultRouter

from watchlist.api import views

router = DefaultRouter()
router.register('stream', views.StreamPlatformAV, basename='stream-platform')
urlpatterns = [
    path('list/', views.WatchListView.as_view(), name='list'),
    path(
        '<int:pk>/', views.WatchListDetailView.as_view(),
        name="movie_detail"
    ),
    path('platform/', views.StreamingPlatFormView.as_view(), name='platform'),
    path(
        "platform/<int:pk>/", views.StreamingPlatformDetailView.as_view(),
        name='platform'
    ),
    path(
        '<int:pk>/review-create/', views.ReviewCreate.as_view(),
        name="review-create"
    ),
    path(
        '<int:pk>/review/', views.ReviewList.as_view(),
        name="review-list"
    ),
    path(
        'review-detail/<int:pk>/', views.ReviewDetail.as_view(),
        name="review-detail"
    ),
    path('', include(router.urls)),
    path('filter-movie', views.FilterMovie.as_view(), name='filter-movie'),
    path('search-movie', views.SearchMovie.as_view(), name='search-movie')
]
