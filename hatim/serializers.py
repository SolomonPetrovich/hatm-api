from rest_framework import serializers
from .models import Juz, Hatim
from user_auth.models import CustomUser as User


class JuzSerializer(serializers.ModelSerializer):
    hatim_id = serializers.ReadOnlyField(source='hatim_id.id')
    user_id  = serializers.ReadOnlyField(source='user_id.id')
    juz_number = serializers.ReadOnlyField()
    status = serializers.ReadOnlyField()
    pageInterval = serializers.ReadOnlyField()
    class Meta:
        model = Juz
        fields = ('id', 'hatim_id', 'user_id', 'juz_number', 'status', 'pageInterval')


class SingleHatimSerializer(serializers.HyperlinkedModelSerializer):
    juz = JuzSerializer(many=True, read_only=True)
    creator_id = serializers.HiddenField(default=serializers.CurrentUserDefault())
    deadline = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")

    class Meta:
        model = Hatim
        fields = ('id', 'creator_id', 'isPublic', 'title', 'description', 'created_at', 'deadline', 'juz')

    def create(self, validated_data):
        user =  self.context['request'].user
        user.hatims_created = 1
        user.save()
        return super().create(validated_data)

class HatimSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Hatim
        fields = ('id', 'creator_id', 'isPublic', 'title', 'description', 'created_at', 'deadline')
