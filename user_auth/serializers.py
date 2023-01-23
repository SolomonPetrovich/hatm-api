from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import CustomUser as User
from hatim.serializers import JuzSerializer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    juz_set = JuzSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'juz_set', 'hatims_created', 'active_hatims')