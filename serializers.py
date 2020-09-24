from rest_framework import serializers
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.hashers import make_password


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length = 100, 
        min_length = 8,
        write_only = True
    )

    class Meta: 
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password']

        def validate(self, attrs):
            email =         attrs.get('email', '')
            username =      attrs.get('username', '')
            first_name =    attrs.get('first_name', '')
            last_name =     attrs.get('last_name', '')
            password =      attrs.get('password', '') #

            if not username.isalnum():
                raise serializers.ValidationError('The username should only contain alphanumeric characters')
            if not first_name.isalpha():
                raise serializers.ValidationError('The First Name should only contain Letters')
            if not last_name.isalpha():
                raise serializers.ValidationError('The Last Name should only contian Letters')
            return attrs

        def create(self, validated_data):            
            return User.objects.create_user(**validated_data)

#From here it will go to the manager to save the user that is why we call the save from the object

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=100, min_length=8, write_only=True)
    username = serializers.CharField(max_length=30, min_length=3, read_only=True)

    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        filtered_user_by_email = User.objects.filter(email=email)
        print(filtered_user_by_email)
        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }

        return super().validate(attrs)