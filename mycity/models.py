from django.db import models
from datetime import datetime
from django.utils import timezone
from mysite.authuser.models import MyUser
import os


POST_TYPES = (
    (1,'Utilidade Pública'),
    (2,'Humor'),
    (3,'Política'),
    (4,'Segurança'),
    (5,'Saúde'),
    (6,'Educação'),
    (7,'Variados')
)

def usr_img_filename(instance, filename):
        return "u/%s/%s" % (instance.user.id, filename)
 
def post_img_filename(instance, filename):
        return "p/%s/%s/%s" % (instance.post.city, instance.post.id,
         filename)


class PostTypeUser(models.Model):
    post_types = models.IntegerField(choices=POST_TYPES, default=1)
    
    def __str__(self):
        return self.post_types
   

class UserProfile(models.Model):
    user = models.OneToOneField(MyUser)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    occupation = models.CharField(max_length=100, null=True,
     blank=True)
    country = models.CharField(max_length=50, default="Brasil")
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    img_usr = models.ImageField(upload_to=usr_img_filename, null=True,
     blank=True, default="pic_profile.jpg")
    post_types = models.ManyToManyField(PostTypeUser)
    validation_key = models.CharField(max_length=50, blank=True, null=True)
    key_expires = models.DateTimeField(default=timezone.now)
     
    def __str__(self):
        return str(self.user)


class MediaFile(models.Model):
    img_post = models.ImageField(
        upload_to=post_img_filename, null=True, blank=True)
 
 
class Post(models.Model):
    author = models.OneToOneField(MyUser)
    text = models.TextField()
    city = models.CharField(max_length=100)
    published_date = models.DateTimeField(default=timezone.now)
    media_file = models.ManyToManyField(MediaFile)
    
    def __str__(self):
        return str(self.id)


class Coment(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    user = models.OneToOneField(MyUser)
    coment_date = models.DateTimeField(default=timezone.now)
    text = models.TextField()
    
    def __str__(self):
        return str(self.id)
