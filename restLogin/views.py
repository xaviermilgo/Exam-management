from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from rest_framework.permissions import IsAuthenticated

import jwt
import json
from ems.settings import SECRET_KEY
from teachers.models import Teacher

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER



class LoginUserView(APIView):
    def post(self, request, *args, **kwargs):
        # @test: curl -X POST -H "Content-Type: application/json" \
        # -d '{"phone_number":"0712345678","password":"pass"}' http://localhost:8008/api-login-user/
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        self.request_validation = self.validate_user(request)
        if self.request_validation:
            payload= jwt_payload_handler(self.user)
            token = {
                'token': jwt.encode(payload, SECRET_KEY),
                'status': 'success'
                }  
            return Response(token)
        return Response({'error': 'Invalid credentials'}, status=401)

    def validate_user(self,r):
        self.phone_number = r.data.get("phone_number")
        self.password = r.data.get("password")
        try:
            self.teacher= Teacher.objects.get(phone_number=self.phone_number)
            self.user= authenticate(username=self.teacher.user.username,password=self.password)
            if self.user:
                return True
        except:
            return False

class PasswordReset(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        self.u=User.objects.get(pk=request.user.pk)
        self.post_data=request.data
        if self.change_password():
            return Response({'success': 'success'})
        return Response({'error': 'Bad request'}, status=400)

    def change_password(self):
        try:
            if len(self.post_data.get("password")) > 0 and self.post_data.get("password")==self.post_data.get("confirmPassword"):
                self.password=self.post_data.get("password")
                self.u.set_password(self.password)
                self.u.save()
                return True
            return False
        except Exception as err:
            print(err)
            return False


def print_headers(request):
    import re
    regex = re.compile('^HTTP_')
    headers=dict((regex.sub('', header), value) for (header, value) 
        in request.META.items() if header.startswith('HTTP_'))
    print(headers)