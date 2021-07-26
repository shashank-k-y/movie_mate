from django.urls import path
from watchlist.views import movie_detail, movie_list

urlpatterns = [
    path('list/', movie_list, name='list'),
    path('<int:pk>', movie_detail, name="movie_detail")
]