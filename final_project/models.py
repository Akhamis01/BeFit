from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models
from PIL import Image
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms.widgets import ClearableFileInput

# User model
class User(AbstractUser):
    pic = models.ImageField(default='default.jpg', upload_to='profile_pics')
    height = models.IntegerField(default=120, validators=[MaxValueValidator(250), MinValueValidator(120)], help_text='Value must be in CM, between 120-250cm')
    weight = models.IntegerField(default=30, validators=[MaxValueValidator(400), MinValueValidator(30)], help_text='Value must be in Kg, between 30-400kg')
    age = models.IntegerField(default=18, validators=[MaxValueValidator(80), MinValueValidator(13)], help_text='Must be between 13-80 years old')
    cv = models.URLField(max_length=120, blank=True)
    special_user = models.BooleanField(default=False)
    professional = models.BooleanField(default=False)

    # This method is for efficiency / faster saves in the profile and images take less storage
    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        img = Image.open(self.pic.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.pic.path)


# Model used for discussions page
class Posts(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    flare = models.CharField(max_length=30, default='General')
    video_url = models.URLField(max_length=300, blank=True)
    likes = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)


# The upvote, downvote, and comment models are used for the discussions page
class Upvotes(models.Model):
    liker = models.ForeignKey('User', on_delete=models.CASCADE)
    post = models.ForeignKey('Posts', on_delete=models.CASCADE)

class Downvotes(models.Model):
    liker = models.ForeignKey('User', on_delete=models.CASCADE)
    post = models.ForeignKey('Posts', on_delete=models.CASCADE)


class Comments(models.Model):
    post = models.ForeignKey('Posts', on_delete=models.CASCADE)
    commenter = models.ForeignKey('User', on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(default=timezone.now)