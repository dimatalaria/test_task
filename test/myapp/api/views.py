from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django_ratelimit.decorators import ratelimit
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

import requests

from .models import Task
from .serializers import TaskSerializer


@api_view(['GET'])
@ratelimit(key='ip', rate='15/m', method='GET', block=True)
def show_tasks(request, user):
    username = User.objects.get(username=user)
    tasks = Task.objects.filter(user=username).select_related('category')
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@ratelimit(key='ip', rate='15/m', method='GET', block=True)
def check_tasks(request, task_id):
    tasks = Task.objects.filter(id=task_id).select_related('category')
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@ratelimit(key='ip', rate='15/m', method='POST', block=True)
def user_register(request):

    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if not username or not password:
        return Response({"detail": "Необходимо указать имя пользователя и пароль."}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"detail": "Пользователь с таким именем уже существует."}, status=status.HTTP_409_CONFLICT)

    user = User.objects.create_user(username=username, password=password, email=email)

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    return Response({
        'access': access_token,
        'refresh': str(refresh),
    },
        status=status.HTTP_201_CREATED)


@api_view(['POST'])
@ratelimit(key='ip', rate='15/m', method='POST', block=True)
def create_task(request):
    if request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@ratelimit(key='ip', rate='15/m', method='POST', block=True)
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return Response({
            'access': access_token,
            'refresh': str(refresh),
        }, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "Неверные данные для входа."}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['DELETE'])
@ratelimit(key='ip', rate='15/m', method='DELETE', block=True)
def delete_task(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    task.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


