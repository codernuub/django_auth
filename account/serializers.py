from rest_framework import serializers
from .models import User

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        db_table = 'users'
        model = User
        fields = ('name', 'email', 'contact',  'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(name=validated_data['name'], email=validated_data['email'], contact=validated_data['contact'], password=validated_data['password'])

        return user