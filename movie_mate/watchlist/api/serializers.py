from rest_framework import serializers

from watchlist.models import WatchList, StreamingPlatform, Review


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        exclude = ('watch_list',)


class WatchListSerializer(serializers.ModelSerializer):
    platform = serializers.CharField(source='platform.name')

    class Meta:
        model = WatchList
        fields = "__all__"


class StreamingPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)

    class Meta:
        model = StreamingPlatform
        fields = "__all__"
