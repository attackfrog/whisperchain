# Whisperchain
A "telephone game" web app.

Whisperchain is now live at http://whisperchain.herokuapp.com/!

Whisperchain is a Django web application which lets users play the classic game of Telephone (a.k.a. "Chinese Whispers") over the internet! Users can create accounts and then form groups, called "chains". "ublic groups looking for more users are displayed to everyone, and non-public groups can only be joined with an invite code or URL. 

Once the chain has reached a specified size, the game begins! The first user is prompted to enter a phrase to start the game. Then, the second user in line is prompted to submit a picture they've drawn as an interpretation of that phrase. Then the third person, seeing only the picture of the person ahead of them, has to come up with a new phrase to describe it. And so on, until everyone has gone twice. Then the game ends, and everyone can see the whole chain of phrases and pictures (and how quickly things got away from that starting phrase!)

## Setup
Whisperchain is designed to run on Heroku, but it can also be run elsewhere. To run it on Heroku, create a Heroku app, set the configuration variables described below, and then deploy this code! To run it on a personal computer, such as for development purposes, it can also be run with `python manage.py runserver`. Make sure to run `python manage.py migrate` and set the configuration variables first.

Whisperchain is set up to use Amazon Web Services S3 as its file storage service, so you'll need an AWS account to run it (unless you configure it to use some other storage.) It is recommended to use app-specific credentials.

### Environment Variables
* `AWS_ACCESS_KEY_ID` = Your AWS access key ID
* `AWS_SECRET_ACCESS_KEY` = Your AWS secret access key
* `SECRET_KEY` = A random 50-character string, to be used for cryptographic purposes

## Structure
### Data
Most data in Whisperchain is stored in three models. 
* `Chain` holds metadata information about a "chain", being an instance of the game. It keeps track of the progression of the game once it starts, and the criteria for joining it as it's forming. 
* `Phrase` holds a user-submitted phrase, along with some metadata, including the chain it's associated with.
* `Picture` is much like `Phrase` but instead holds information about a user-uploaded image file. That includes the image's dimensions.

The actual image file data is stored "in the cloud," in a bucket on Amazon's S3 storage service.

### Layout
There are two main "sections" of the Whisperchain site once logged in: a main page which displays the logged-in user's currently active chains and public chains looking for members; and the page for each chain. Each user also has a profile page which displays all the chains they have taken part in. Additional pages include login/signup pages and a credits page.

### Rendering
The "back-end logic" is handled in `views.py`. Routes there receive and process submitted data from the user, and retrieve and process data from the database as requested. Most routes decide what information to send to the template based purely on the request method ("POST" vs. "GET") and whether the user is logged in, but `chain` also looks at whether the chain is still looking for more users in deciding which template to show, and what information to pass to it. Others, such as `index`, are selective about which chains they pass to be displayed.

The templates make most of the decisions on what to display to the user, whether it is which buttons to show in the nav bar or which images or phrases to display to the user on a chain's page (and which to replace with a placeholder.)

All of Whisperchain's forms are rendered using Django's forms functionality, which lets their fields be identified by the appropriate data model.

Whisperchain is styled using Bootstrap 4, with a bit of additional custom styling.