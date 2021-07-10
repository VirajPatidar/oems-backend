from rest_framework import serializers
from .models import *

class QuizSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quiz
        fields = '__all__'