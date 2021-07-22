from rest_framework import serializers

from .models import SharedFolder

class UploadToSharedFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedFolder
        fields=['title', 'filefield', 'timestamp', 'class_id']

class GetSFFilesSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField('getUsername')

    def getUsername(self, obj):
        return obj.added_by.name

    class Meta:
        model = SharedFolder
        fields = ['id', 'title', 'filefield', 'added_by', 'timestamp', 'name']