from django.contrib.auth.models import User

from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    password_2 = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_2']
        extra_kwargs = {
            'password': {"write_only": True}
        }

    def save(self):
        email = self.validated_data['email']
        password = self.validated_data['password']
        if self.validated_data['password_2'] != password:
            raise serializers.ValidationError("Password didn't match")

        user = User.objects.filter(email=email)
        if user.exists():
            raise serializers.ValidationError(
                "User with the given email already exists"
            )

        account = User(email=email, username=self.validated_data['username'])
        account.set_password(password)
        account.save()
        return account
