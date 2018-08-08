from django.db import models
from django.contrib.auth import get_user_model

MAX_CHAIN_NAME_LENGTH = 20
CHAIN_CODE_LENGTH = 6 # must be an even number, due to how the hash works
MAX_USERS_PER_CHAIN = 10

class Chain(models.Model):
    users = models.ManyToManyField(get_user_model(), related_name="chains")
    maxUsers = models.IntegerField(verbose_name="Maximum Users in Chain")
    isOpen = models.BooleanField(default=True)
    length = models.IntegerField(default=2)
    currentPosition = models.IntegerField(default=0)
    isPublic = models.BooleanField(verbose_name="Make Chain Public")
    name = models.CharField(max_length=MAX_CHAIN_NAME_LENGTH)
    code = models.CharField(max_length=CHAIN_CODE_LENGTH, unique=True)

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
    height = models.PositiveIntegerField()
    width = models.PositiveIntegerField()
    data = models.ImageField(upload_to="images/%Y/%m", height_field="height", width_field="width")

class Phrase(Submission):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_DEFAULT, default="[Deleted User]", related_name="phrases")
    chain = models.ForeignKey(Chain, on_delete=models.CASCADE, related_name="phrases")
    text = models.TextField()
