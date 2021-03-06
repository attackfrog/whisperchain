from time import strftime

# Gives which player's turn it is at a certain position in the chain
# This should ideally be semi-randomized (but consistently), such that each user has both an odd and even position
# (This version obviously doesn't do that)
# Users should be a QuerySet
def nextPlayer(currentPosition, Users):
    numUsers = len(Users)
    return Users[currentPosition % numUsers]

# Returns a formatted location to upload an image to in file storage
# https://docs.djangoproject.com/en/2.0/ref/models/fields/#django.db.models.FileField.upload_to
def imagePath(instance, filename):
    return strftime(f"images/{instance.user}/%Y/%m/%H.%M.%S-{filename}")
