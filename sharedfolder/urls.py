from django.urls import path
from .views import *

urlpatterns = [
    path("uploadfile", fileUploadView.as_view(), name='uploadfile'),
    path("<int:class_id>", getSFFiles.as_view(), name='get-sf-files'),
    path('delete-shared-file/<int:file_id>', DeleteSFFileView.as_view(), name='delete-shared-file')
]