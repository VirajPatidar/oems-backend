from django.shortcuts import render
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from .models import Chat
from .serializers import (
    ChatMessageSerializer
)
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

class HandleMessageView(generics.GenericAPIView):
    serializer_class = ChatMessageSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        class_data = serializer.data
        return Response(class_data, status=status.HTTP_201_CREATED)



class GetMessageView(generics.GenericAPIView):
    serializer_class = ChatMessageSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, class_id):

        messages = Chat.objects.filter(class_id = class_id).order_by('timestamp')
        print(len(messages))
        if len(messages) == 0 :
            return Response({'response':'Invalid class ID'})

        serializer = ChatMessageSerializer(instance=messages, many=True)
        return Response(serializer.data)