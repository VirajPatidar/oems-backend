#General imports
from django.shortcuts import render
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponsePermanentRedirect
import os
from decouple import config
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.conf import settings
from django.db.models import F

#Imports from other files
from .models import User, Student, Teacher
from .utils import Util
from .serializers import (
    RegisterSerializer,
    EmailVerificationSerializer,
    LoginSerializer,
    LogoutSerializer,
    ChangePasswordSerializer,
    ResetPasswordEmailRequestSerializer,
    SetNewPasswordSerializer,
    UpdateAvatarSerializer
)

from klass.models import Study, Classes

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_shemes = [config('APP_SCHEME'), 'http', 'https']

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user)
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = 'Hi '+user.name + \
            ' Use the link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}

        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        redirect_url = "https://www.google.com/"  #this will be frontend url
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            # return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
            return CustomRedirect(redirect_url+'?Success=True&message=Email activated')
        except jwt.ExpiredSignatureError as identifier:
            # return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
            return CustomRedirect(redirect_url+'?Success=False&message=Activation Expired')
        except jwt.exceptions.DecodeError as identifier:
            # return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
            return CustomRedirect(redirect_url+'?Success=False&message=Invalid token')

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.data
        email = request.data.get('email', '')
        user = User.objects.get(email=email)
        profile_picture = user.avatar.url
        user_id = user.pk
        if user.user_type == "student":
            stu = Student.objects.get(email=user.email)
            student_email = email
            student_name = user.name
            user_type = user.user_type
            student_id = stu.pk
            class_details = Study.objects.select_related('class_id').values('class_id', 'student_id', class_name=F('class_id__name')).filter(student_id=student_id)
            class_response=[]
            for i in class_details:
                class_obj=Classes.objects.get(pk=i['class_id'])
                dict1={
                    'class_id': i['class_id'],
                    'class_name': i['class_name'],
                    'teacher_name':class_obj.teacher_id.user.name
                }
                class_response.append(dict1)
            return Response({'user_data': user_data, 'class_details': class_response, 'user id':user_id, 'student email':student_email, 'student name':student_name, 'user_type':user_type, 'student id': student_id, 'profile picture': profile_picture}, status=status.HTTP_200_OK)
        else:
            tea = Teacher.objects.get(email=user.email)
            teacher_email = email
            teacher_name = user.name
            user_type = user.user_type
            teacher_id = tea.pk
            class_details = Classes.objects.filter(teacher_id=teacher_id)
            class_response=[]
            for i in class_details:
                dict1={
                    'class_id': i.pk,
                    'class_name': i.name,
                }
                class_response.append(dict1)
            return Response({'user_data': user_data, 'class_details': class_response, 'user id':user_id, 'teacher email':teacher_email, 'teacher name':teacher_name, 'user_type':user_type, 'teacher id': teacher_id, 'profile picture': profile_picture}, status=status.HTTP_200_OK)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message':'Logged Out Succesfully'}, status=status.HTTP_204_NO_CONTENT)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'message': 'Password updated successfully',
            }

            return Response(response, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            redirect_url = "https://www.google.com/"  #this will be frontend url           
            absurl = 'http://'+current_site + relativeLink
            email_body = 'Hello, \n Use link below to reset your password  \n' + absurl+"?redirect_url="+redirect_url 
            data = {'email_body': email_body, 'to_email': user.email,                     
                    'email_subject': 'Reset your passsword'}                                                      
            Util.send_email(data)                                                                                          
            return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)         
        return Response({'failed': 'invalid email'}, status=status.HTTP_400_BAD_REQUEST)         

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 
                                                                                                                           
class PasswordTokenCheckAPI(generics.GenericAPIView):                                                                      
    def get(self, request, uidb64, token):                                                                                 
                                                                                                                            
        redirect_url = request.GET.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return CustomRedirect(redirect_url+'?token_valid=False')
                #return Response({'error':'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)

            #return Response({'success':True, 'message':'Credentials Valid', 'uidb64':uidb64, 'token':token}, status=status.HTTP_200_OK)
            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(redirect_url+'?token_valid=True&message=Credentials Valid&uidb64='+uidb64+'&token='+token)
            else:
                return CustomRedirect(redirect_url+'?token_valid=False')
            

        except DjangoUnicodeDecodeError as identifier:
            #return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)
            return CustomRedirect(redirect_url+'?token_valid=False')

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class UpdateAvatarView(generics.UpdateAPIView):
    serializer_class = UpdateAvatarSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, format=None, *args, **kwargs):
        print(request.data)
        self.object = self.get_object()
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            profile_url=os.path.join(settings.BASE_DIR, self.object.avatar.url)
            self.object.avatar = request.data.get('avatar')
            self.object.save()
            
            if os.path.exists(profile_url):
                os.remove(profile_url)
                
            response = {
                'status': 'success',
                'message': 'Profile Picture updated successfully',
            }

            return Response(response, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

