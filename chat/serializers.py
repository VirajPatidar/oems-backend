from rest_framework import serializers
from .models import Chat

class ChatMessageSerializer(serializers.ModelSerializer):

    profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = '__all__'
    
    def get_profile_picture(self, obj):
        return obj.user_id.avatar.url