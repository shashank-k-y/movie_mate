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

from watchlist.models import WatchList, StreamingPlatform, Review
from watchlist.api.serializers import (
    ReviewSerializer,
    WatchListSerializer,
    StreamingPlatformSerializer
)
from watchlist.api.permissions import (
    IsReviewUserOrReadOnly,
    IsAdminOrReadOnly
)
from watchlist.api.throttling import ReviewCreateThrottle, ReviewListThrottle
from watchlist.api.pagination import WatchListPagination, WatchListLimitOffsetPagination


class WatchListView(APIView):

    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        movies = WatchList.objects.all()
        paginator = WatchListPagination()
        result_page = paginator.paginate_queryset(queryset=movies, request=request)
        serializer = WatchListSerializer(result_page, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            platform = StreamingPlatform.objects.get(
                name=request.data['platform']
            )
        except ObjectDoesNotExist:
            return Response(
                {"error": "platform does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = WatchListSerializer(
            data=request.data, context={"platform": platform}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class WatchListDetailView(APIView):

    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response(
                {"error": "Movie does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = WatchListSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response(
                {"error": "Movie does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response(
                {"error": "Movie does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StreamingPlatFormView(APIView):

    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        movies = StreamingPlatform.objects.all()
        serializer = StreamingPlatformSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StreamingPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class StreamingPlatformDetailView(APIView):

    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            platform = StreamingPlatform.objects.get(pk=pk)
        except StreamingPlatform.DoesNotExist:
            return Response(
                {"error": "Platform does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        serialzer = StreamingPlatformSerializer(platform)
        return Response(serialzer.data)

    def put(self, request, pk):
        try:
            platform = StreamingPlatform.objects.get(pk=pk)
        except StreamingPlatform.DoesNotExist:
            return Response(
                {"error": "Platform does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = StreamingPlatformSerializer(platform, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, pk):
        try:
            movie = StreamingPlatform.objects.get(pk=pk)
        except StreamingPlatform.DoesNotExist:
            return Response(
                {"error": "Movie does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin,
# generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        try:
            watch_list = WatchList.objects.get(id=pk)
        except WatchList.DoesNotExist:
            raise ValidationError("Movie does not exists !")

        user = self.request.user
        review = Review.objects.filter(watch_list=watch_list, reviewer=user)
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
    serializer_class = ReviewSerializer
    throttle_classes = [ReviewListThrottle]

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watch_list=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'


# class StreamPlatformAV(viewsets.ViewSet):
#     def list(self, request):
#         query_set = StreamingPlatform.objects.all()
#         serializer = StreamingPlatformSerializer(query_set, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk):
#         query_set = StreamingPlatform.objects.all()
#         stream_platform = get_object_or_404(query_set, pk=pk)
#         serializer = StreamingPlatformSerializer(stream_platform)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = StreamingPlatformSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(
#                  serializer.errors,
#                  status=status.HTTP_400_BAD_REQUEST
#             )
#         serializer.save()
#         return Response(serializer.data)


class StreamPlatformAV(viewsets.ModelViewSet):
    queryset = StreamingPlatform.objects.all()
    serializer_class = StreamingPlatformSerializer
    permission_classes = [IsAdminOrReadOnly]


class FilterMovie(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    pagination_class = WatchListLimitOffsetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'platform__name']


class SearchMovie(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'platform__name']
