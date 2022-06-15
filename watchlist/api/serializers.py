from rest_framework import serializers

from watchlist.models import WatchList, StreamingPlatform, Review


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        exclude = ('watch_list',)


class WatchListSerializer(serializers.ModelSerializer):
    platform = serializers.CharField(source="platform.name")

    class Meta:
        model = WatchList
        fields = "__all__"

    def create(self, validated_data):
        platform = self.context['platform']
        validated_data.update(platform=platform)
        return WatchList.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.storyline = validated_data.get(
            "storyline", instance.storyline
        )
        instance.active = validated_data.get("active", instance.active)
        instance.save()
        return instance


class StreamingPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)

    class Meta:
        model = StreamingPlatform
        fields = "__all__"
