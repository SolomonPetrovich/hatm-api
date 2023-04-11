import datetime
from rest_framework import serializers
from .models import Juz, Hatm


class JuzSerializer(serializers.ModelSerializer):
    hatm_id = serializers.CharField(read_only=True , source='hatm_id.id')
    juz_number = serializers.IntegerField(read_only=True)
    type = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    deadline = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    user_id = serializers.CharField(read_only=True, source='user_id.id')

    class Meta:
        model = Juz
        fields = ('id', 'hatm_id',  'juz_number', 'status', 'type', 'deadline', 'user_id')


class JuzTakeSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.UUIDField(), write_only=True)
    days = serializers.IntegerField(write_only=True)


class HatmSerializer(serializers.HyperlinkedModelSerializer):
    juz = JuzSerializer(many=True, read_only=True)
    is_public = serializers.BooleanField(required=True)
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=500)
    deadline = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    completed = serializers.SerializerMethodField()
    in_progress = serializers.SerializerMethodField()
    free = serializers.SerializerMethodField()

    class Meta:
        model = Hatm
        fields = ('id','is_public', 'title', 'description', 'deadline','completed', 'in_progress', 'free', 'juz')

    def get_completed(self, obj) -> int:
        return obj.juz.filter(status='completed').count()
        
    def get_free(self, obj) -> int:
        return obj.juz.filter(status='free').count()
    
    def get_in_progress(self, obj) -> int:
        return obj.juz.filter(status='in Progress').count()