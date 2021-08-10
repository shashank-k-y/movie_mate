from rest_framework import serializers

from watchlist.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"

    def validate(self, data):
        if data["name"] == data["description"]:
            raise serializers.ValidationError(
                "Name and Description can not be same."
            )
        return data

    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Name is too Short.")
