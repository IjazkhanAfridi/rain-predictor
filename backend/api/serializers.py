from rest_framework import serializers
from django.contrib.auth.models import User
from .models import PredictionRequest


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class PredictionRequestSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = PredictionRequest
        fields = [
            'id', 
            'user', 
            'user_email', 
            'location', 
            'date', 
            'prediction_result', 
            'confidence',
            'weather_data',
            'created_at', 
            'updated_at'
        ]
        read_only_fields = ['id', 'user', 'user_email', 'created_at', 'updated_at']


class PredictionInputSerializer(serializers.Serializer):
    location = serializers.CharField(max_length=255)
    date = serializers.DateField()

    def validate_location(self, value):
        if not value.strip():
            raise serializers.ValidationError("Location cannot be empty.")
        return value.strip()
