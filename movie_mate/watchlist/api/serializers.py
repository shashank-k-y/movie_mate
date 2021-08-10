from rest_framework import serializers

from watchlist.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    name_length = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = "__all__"

    def get_name_length(self, object):
        return len(object.name)
