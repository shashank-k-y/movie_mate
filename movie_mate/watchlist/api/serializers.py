from rest_framework import serializers
from .validators import validate_name

from watchlist.models import Movie

class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(validators=[validate_name])
    description = serializers.CharField()
    active = serializers.BooleanField()

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.name)
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance

    def validate(self, data):
        if data["name"] == data["description"]:
            raise serializers.ValidationError("Name and Description can not be same.")
        return data
