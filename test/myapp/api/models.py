import os

from django.db import models
from django.contrib.auth.models import User

import hashlib
import time

class Category(models.Model):
    id = models.CharField(primary_key=True, max_length=24, editable=False)
    name = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.generate_key()
        super().save(*args, **kwargs)

    def generate_key(self):
        timestamp = str(int(time.time() * 1000))
        pid = str(os.getpid())
        combined = timestamp + pid
        return hashlib.sha256(combined.encode()).hexdigest()[:24]

    def __str__(self):
        return self.name


class Task(models.Model):
    id = models.CharField(primary_key=True, max_length=8, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_notified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.generate_key()
        super().save(*args, **kwargs)

    def generate_key(self):
        timestamp = str(int(time.time() * 1000))
        pid = str(os.getpid())
        combined = timestamp + pid
        return hashlib.sha256(combined.encode()).hexdigest()[:8]

    def __str__(self):
        return self.user.username