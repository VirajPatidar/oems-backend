from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status, permissions, generics
import os
from django.conf import settings
# Create your views here.

# Parsers help your views to parse the data submitted in a specific format. Basically they map the Content-Type header of the HTTP request to the code required to parse that type into a python structure that your Serializer can understand

from .serializers import UploadToSharedFolderSerializer, GetSFFilesSerializer
from .models import SharedFolder
from klass.models import Classes


class fileUploadView(CreateAPIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UploadToSharedFolderSerializer

    def perform_create(self, serializer):
        return serializer.save(added_by=self.request.user)

class getSFFiles(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GetSFFilesSerializer
    def get(self, request, class_id):
        allFiles = SharedFolder.objects.filter(class_id=class_id).order_by('-timestamp')
        if len(allFiles)==0:
            return Response({
                'message':'Shared folder is empty'
            }, status=status.HTTP_204_NO_CONTENT)
        
        allFilesSerialised = GetSFFilesSerializer(instance=allFiles, many=True)

        return Response(allFilesSerialised.data, status=status.HTTP_200_OK)










        # isOwner = False
        # class_obj = Classes.objects.get(id=class_id)
        # allfiles = SharedFolder.objects.filter(class_id=class_obj).order_by('-timestamp')
        # result=[]
        # for allfile in allfiles:
        #     if allfile.added_by==request.user:
        #         isOwner = True
        #     dict1={
        #         'id': allfile.pk,
        #         'title': allfile.title,
        #         'filefield': allfile.filefield,
        #         'timestamp': allfile.timestamp,
        #         'isOwner':isOwner,
        #     }
        #     result.append(dict1)
        # if len(result)!=0:
        #     return Response({
        #         'files':result,
        #     }, status=status.HTTP_200_OK)
        # else:
        #     return Response({
        #         'message': 'shared folder is empty'
        #     }, status=status.HTTP_204_NO_CONTENT)


class DeleteSFFileView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        fileid= request.data['id']
        sf_obj = SharedFolder.objects.filter(pk=fileid)
        if len(sf_obj)!=0:
            if sf_obj[0].added_by != request.user:
                return Response({
                    'message': 'You can not delete this file'
                }, status=status.HTTP_403_FORBIDDEN)
            file_url=os.path.join(settings.BASE_DIR, sf_obj[0].filefield.url)
            # print(file_url)
            # print(sf_obj[0].filefield.url)
            sf_obj[0].delete()
            if os.path.exists(file_url):
                print(True)
                os.remove(file_url)
            return Response({
                'message': 'File deleted successfully'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': 'Invalid Id'
            }, status=status.HTTP_204_NO_CONTENT)