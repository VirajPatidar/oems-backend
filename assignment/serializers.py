from rest_framework import serializers
from .models import *
from klass.models import Study

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'

class AssignmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'name', 'due_on']


class GetAssignmentSerializer(serializers.ModelSerializer):

    assignment_status = serializers.SerializerMethodField()

    class Meta:
        model = Assignment
        fields = '__all__'

    def get_assignment_status(self, obj):
        return obj.assignment_status()