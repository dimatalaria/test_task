from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import Category, Task
from django.contrib.auth.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create_user(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
        )
        return user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name"
        ]

class TaskSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    category = CategorySerializer()

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'due_date', 'user', 'category', 'is_notified', 'created_at')

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        category_name = category_data['name']
        category, created = Category.objects.get_or_create(name=category_name)
        validated_data['category'] = category
        task = Task.objects.create(**validated_data)
        return task