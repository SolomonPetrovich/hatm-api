from rest_framework import serializers
from .models import Juz, Hatim
from user_auth.models import CustomUser as User


class JuzSerializer(serializers.ModelSerializer):
    hatim_id = serializers.ReadOnlyField(source='hatim_id.id')
    juz_number = serializers.ReadOnlyField()
    
    class Meta:
        model = Juz
        fields = ('id', 'hatim_id', 'user_id', 'juz_number', 'status', 'type')


class SingleHatimSerializer(serializers.HyperlinkedModelSerializer):
    juz = JuzSerializer(many=True, read_only=True)
    creator_id = serializers.ReadOnlyField(source='creator_id.id')
    
    class Meta:
        model = Hatim
        fields = ('id', 'creator_id','isCompleted', 'isPublic', 'title', 'description', 'deadline', 'juz')

    def create(self, validated_data):
        user = self.context['request'].user
        user.hatims_created = user.hatims_created + 1
        user.active_hatims = user.active_hatims + 1
        user.save()
        return super().create(validated_data)


class HatimSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Hatim
        fields = ('id', 'creator_id', 'isPublic', 'title', 'description', 'deadline')
