from django.http import response
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from watchlist.models import Movie
from watchlist.api.serializers import MovieSerializer

@api_view(['GET', 'POST'])
def movie_list(request):
    if request.method == "GET":
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail(request, pk):
    try:
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return Response({"error": "Movie does not exist"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    