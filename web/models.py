from django.db import models
from django.contrib.auth import get_user_model

class Chain(models.Model):
    users = models.ManyToManyField(get_user_model(), related_name="chains")
    length = models.IntegerField()
    currentPosition = models.IntegerField()
    isPublic = models.BooleanField()

class Picture(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_DEFAULT, default="[Deleted User]", related_name="pictures")
    chain = models.ForeignKey(Chain, on_delete=models.CASCADE, related_name="pictures")
    position = models.IntegerField()
    timestamp = models.DateTimeField(auto_now=True)
    data = models.ImageField(upload_to="images/%Y/%m")

class Phrase(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_DEFAULT, default="[Deleted User]", related_name="phrases")
    chain = models.ForeignKey(Chain, on_delete=models.CASCADE, related_name="phrases")
    position = models.IntegerField()
    timestamp = models.DateTimeField(auto_now=True)
    text = models.TextField()
