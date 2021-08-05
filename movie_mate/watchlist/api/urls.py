from django.urls import path
from watchlist.api.views import movie_list, movie_detail

urlpatterns = [
    path('list/', movie_list, name='list'),
    path('<int:pk>', movie_detail, name="movie_detail")
]