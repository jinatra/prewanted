import re
import json
import bcrypt
import jwt

from django.shortcuts import render
from django.views     import View
from django.http      import JsonResponse

from users.models import User

class SignUpView(View):
    def post(self, request):
        data     = json.loads(request.body)
        email    = data['email']
        password = data['password']
        nickname = data['nickname']

        if not re.match('^[a-zA-Z\d+-.]+@[a-zA-Z\d+-.]+\.[a-zA-Z]{2,3}$', email):
            return JsonResponse({'STATUS':'ERROR', 'MESSAGE':'Wrong E-Mail Form'}, status=400)

        if not re.match('^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{10,}$', password):
            return JsonResponse({'STATUS':'ERROR', 'MESSAGE':'Wrong E-Mail Form'}, status=400)

        if User.objects.filter(email = email).exists():
                return JsonResponse({'STATUS':'ERROR', 'MESSAGE':'Existing E-Mail'}, status = 409)
        
        if User.objects.filter(nickname = nickname).exists():
                return JsonResponse({'STATUS':'ERROR', 'MESSAGE':'Existing Nickname'}, status = 409)

        decoded_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt().decode('utf-8'))

        User.objects.create(
            email    = email,
            password = decoded_password,
            nickname = nickname,
        )

        return JsonResponse({'STATUS':'SUCCESS', 'MESSAGE':'User Created!'}, status=201)
