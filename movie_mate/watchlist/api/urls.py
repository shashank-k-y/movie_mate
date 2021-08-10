from django.urls import path
from watchlist.api.views import (
    WatchListDetailView,
    WatchListView,
    StreamingPlatFormView,
    StreamingPlatformDetailView
)

urlpatterns = [
    path('list/', WatchListView.as_view(), name='list'),
    path('<int:pk>', WatchListDetailView.as_view(), name="movie_detail"),
    path('platform/', StreamingPlatFormView.as_view(), name='platform'),
    path(
        "platform/<int:pk>",
        StreamingPlatformDetailView.as_view(),
        name='platform'
    )
]
