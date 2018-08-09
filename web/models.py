from django.db import models
from django.contrib.auth import get_user_model

from .helpers import imagePath

MAX_CHAIN_NAME_LENGTH = 20
CHAIN_CODE_LENGTH = 6 # must be an even number, due to how the hash works
MAX_USERS_PER_CHAIN = 10

# Stores metadata about user groups (chains)
class Chain(models.Model):
    users = models.ManyToManyField(get_user_model(), related_name="chains")
    maxUsers = models.IntegerField(verbose_name="Maximum Users in Chain")
    isOpen = models.BooleanField(default=True) # chain still needs more users to begin
    isActive = models.BooleanField(default=True) # user still have more phrases and pictures to submit
    length = models.IntegerField(default=2) # currently set to 2x the number of users, but this could be changed
    currentPosition = models.IntegerField(default=0) # how many submissions have been submitted, essentially
    isPublic = models.BooleanField(verbose_name="Make Chain Public") # whether the chain should show up under "public chains"
    name = models.CharField(max_length=MAX_CHAIN_NAME_LENGTH)
    code = models.CharField(max_length=CHAIN_CODE_LENGTH, unique=True)

    def __str__(self):
        return f"{self.name} ({self.currentPosition}/{self.length})"

# Base class for picture and phrase submissions. Not used by itself
class Submission(models.Model):
    position = models.IntegerField()
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.user} on {self.timestamp}" # pylint: disable=no-member

# Picture submission data. Actual image files are stored in FILE_STORAGE, and accessed through data.url
class Picture(Submission):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_DEFAULT, default="[Deleted User]", related_name="pictures")
    chain = models.ForeignKey(Chain, on_delete=models.CASCADE, related_name="pictures")
    height = models.PositiveIntegerField(blank=True, null=True) # autopopulates on image upload
    width = models.PositiveIntegerField(blank=True, null=True) # autopopulates on image upload
    data = models.ImageField(upload_to=imagePath, height_field="height", width_field="width")

# Phrase submission data
class Phrase(Submission):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_DEFAULT, default="[Deleted User]", related_name="phrases")
    chain = models.ForeignKey(Chain, on_delete=models.CASCADE, related_name="phrases")
    text = models.TextField()
