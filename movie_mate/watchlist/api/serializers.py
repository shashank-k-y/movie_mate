from django.db.models import fields
from rest_framework import serializers
from .validators import validate_name

from watchlist.models import Movie

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"
    

    def validate(self, data):
        if data["name"] == data["description"]:
            raise serializers.ValidationError("Name and Description can not be same.")
        return data
