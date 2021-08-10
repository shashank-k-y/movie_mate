from rest_framework import serializers

from watchlist.models import WatchList, StreamingPlatform


class WatchListSerializer(serializers.ModelSerializer):

    class Meta:
        model = WatchList
        fields = "__all__"

class StreamingPlatformSerializer(serializers.ModelSerializer):

    class Meta:
        model = StreamingPlatform
        fields = "__all__"

