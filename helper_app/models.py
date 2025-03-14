from django.db import models


# Create your models here.
class Chats(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Messages(models.Model):
    USER_TYPES = (
        ('user', 'User'),
        ('assistant', 'Assistant'),
    )
    id = models.AutoField(primary_key=True)
    chat_id = models.ForeignKey(Chats, on_delete=models.CASCADE)
    user = models.CharField(max_length=10, choices=USER_TYPES, null=False, blank=False)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text