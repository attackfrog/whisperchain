from django.db import models
from django.contrib.auth import get_user_model

class Chain(models.Model):
    users = models.ManyToManyField(get_user_model(), related_name="chains")
    length = models.IntegerField()
    currentPosition = models.IntegerField()
    isPublic = models.BooleanField()
    name = models.CharField(max_length=15)
    code = models.CharField(max_length=6, unique=True)

    def __str__(self):
        return f"{self.name} ({self.currentPosition}/{self.length})"

class Submission(models.Model):
    position = models.IntegerField()
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.user} on {self.timestamp}" # pylint: disable=no-member

class Picture(Submission):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_DEFAULT, default="[Deleted User]", related_name="pictures")
    chain = models.ForeignKey(Chain, on_delete=models.CASCADE, related_name="pictures")
    data = models.ImageField(upload_to="images/%Y/%m")

class Phrase(Submission):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_DEFAULT, default="[Deleted User]", related_name="phrases")
    chain = models.ForeignKey(Chain, on_delete=models.CASCADE, related_name="phrases")
    text = models.TextField()
