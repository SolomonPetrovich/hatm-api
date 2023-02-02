from rest_framework import serializers
from .models import Juz, Hatm
from user_auth.models import CustomUser as User


class JuzSerializer(serializers.ModelSerializer):
    hatm_id = serializers.ReadOnlyField(source='hatm_id.id')
    juz_number = serializers.ReadOnlyField()
    
    class Meta:
        model = Juz
        fields = ('id', 'hatm_id', 'user_id', 'juz_number', 'status', 'type')


class HatmSerializer(serializers.HyperlinkedModelSerializer):
    juz = JuzSerializer(many=True, read_only=True)
    creator_id = serializers.ReadOnlyField(source='creator_id.id')
    isPublic = serializers.BooleanField(required=True)
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=500)
    deadline = serializers.DateField()

    class Meta:
        model = Hatm
        fields = ('id', 'creator_id', 'isPublic', 'title', 'description', 'deadline', 'juz')