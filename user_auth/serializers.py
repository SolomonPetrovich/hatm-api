from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import CustomUser as User
from hatim.serializers import JuzSerializer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    juz_set = JuzSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('email', 'nickname', 'juz_set', 'hatims_created', 'active_hatims')


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    nickname = serializers.CharField(required=True)
    password = serializers.CharField(required=True , max_length=128, min_length=6, write_only=True , style={'input_type': 'password'})
    re_password = serializers.CharField(required=True, max_length=128, min_length=6, write_only=True)


    class Meta:
        model = User
        fields = ('email', 'nickname', 'password', 're_password')
        extra_kwargs = {
            'password': {'write_only': True},
            're_password': {'write_only': True}
        }

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already exists')
        return email

    def validate_password(self, password):
        if password != self.initial_data['re_password']:
            raise serializers.ValidationError('Passwords do not match')
        return password

    def create(self, validated_data):
        hashed_password = make_password(validated_data['password'])

        user = User.objects.create(
            email=validated_data['email'],
            nickname=validated_data['nickname'],
            password=hashed_password
        )
        
        return user


class InputSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    nickname = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('email', 'nickname')
    