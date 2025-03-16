

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .import views


urlpatterns = [
    path('task/<str:user>', views.show_tasks, name='task'),
    path('create/', views.create_task, name='create'),
    path('delete/<str:pk>/', views.delete_task, name='delete_task'),
    path('check_task/<str:task_id>', views.check_tasks, name='check_task'),
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]