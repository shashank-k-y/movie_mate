from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle
from rest_framework import filters

from watchlist import models
from watchlist.api import serializers
from watchlist.api import permissions
from watchlist.api import throttling
from watchlist.api import pagination


class WatchListView(APIView):

    permission_classes = [permissions.IsAdminOrReadOnly]

    def get(self, request):
        movies = models.WatchList.objects.all()
        paginator = pagination.WatchListPagination()
        result_page = paginator.paginate_queryset(
            queryset=movies, request=request
        )
        serializer = serializers.WatchListSerializer(result_page, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            platform = models.StreamingPlatform.objects.get(
                name=request.data['platform']
            )
        except ObjectDoesNotExist:
            return Response(
                {"error": "platform does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = serializers.WatchListSerializer(
            data=request.data, context={"platform": platform}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class WatchListDetailView(APIView):

    permission_classes = [permissions.IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            movie = models.WatchList.objects.get(pk=pk)
        except models.WatchList.DoesNotExist:
            return Response(
                {"error": "Movie does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = serializers.WatchListSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            movie = models.WatchList.objects.get(pk=pk)
        except models.WatchList.DoesNotExist:
            return Response(
                {"error": "Movie does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = serializers.WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        try:
            movie = models.WatchList.objects.get(pk=pk)
        except models.WatchList.DoesNotExist:
            return Response(
                {"error": "Movie does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StreamingPlatFormView(APIView):

    permission_classes = [permissions.IsAdminOrReadOnly]

    def get(self, request):
        movies = models.StreamingPlatform.objects.all()
        serializer = serializers.StreamingPlatformSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.StreamingPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class StreamingPlatformDetailView(APIView):

    permission_classes = [permissions.IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            platform = models.StreamingPlatform.objects.get(pk=pk)
        except models.StreamingPlatform.DoesNotExist:
            return Response(
                {"error": "Platform does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        serialzer = serializers.StreamingPlatformSerializer(platform)
        return Response(serialzer.data)

    def put(self, request, pk):
        try:
            platform = models.StreamingPlatform.objects.get(pk=pk)
        except models.StreamingPlatform.DoesNotExist:
            return Response(
                {"error": "Platform does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = serializers.StreamingPlatformSerializer(
            platform, request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        try:
            movie = models.StreamingPlatform.objects.get(pk=pk)
        except models.StreamingPlatform.DoesNotExist:
            return Response(
                {"error": "Platform does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewCreate(generics.CreateAPIView):
    serializer_class = serializers.ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [throttling.ReviewCreateThrottle]

    def get_queryset(self):
        return models.Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        try:
            watch_list = models.WatchList.objects.get(id=pk)
        except models.WatchList.DoesNotExist:
            raise ValidationError("Movie does not exists !")

        user = self.request.user
        review = models.Review.objects.filter(
            watch_list=watch_list, reviewer=user
        )
        if review.exists():
            raise ValidationError("You have already reviewed this movie")

        if watch_list.number_of_ratings == 0:
            watch_list.average_rating = serializer.validated_data['ratings']
        else:
            watch_list.average_rating = (
                watch_list.average_rating +
                serializer.validated_data['ratings']
            ) / 2
        watch_list.number_of_ratings += 1
        watch_list.save()

        serializer.save(watch_list=watch_list, reviewer=user)


class ReviewList(generics.ListAPIView):
    serializer_class = serializers.ReviewSerializer
    throttle_classes = [throttling.ReviewListThrottle]

    def get_queryset(self):
        pk = self.kwargs['pk']
        return models.Review.objects.filter(watch_list=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = [permissions.IsReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'


class StreamPlatformAV(viewsets.ModelViewSet):
    queryset = models.StreamingPlatform.objects.all()
    serializer_class = serializers.StreamingPlatformSerializer
    permission_classes = [permissions.IsAdminOrReadOnly]


class FilterMovie(generics.ListAPIView):
    queryset = models.WatchList.objects.all()
    serializer_class = serializers.WatchListSerializer
    pagination_class = pagination.WatchListLimitOffsetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'platform__name']


class SearchMovie(generics.ListAPIView):
    queryset = models.WatchList.objects.all()
    serializer_class = serializers.WatchListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'platform__name']
