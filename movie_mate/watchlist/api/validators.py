from rest_framework import serializers


def validate_name(value):
    if len(value) < 2:
        raise serializers.ValidationError("Name is too Short.")
