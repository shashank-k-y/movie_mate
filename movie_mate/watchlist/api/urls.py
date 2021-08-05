from django.urls import path
from watchlist.api.views import MovieDetailAV, MovieListAV

urlpatterns = [
    path('list/', MovieListAV.as_view(), name='list'),
    path('<int:pk>', MovieDetailAV.as_view(), name="movie_detail")
]
