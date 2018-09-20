from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.

class Course(models.Model):
    title = models.CharField(max_length = 200)
    credits = models.PositiveSmallIntegerField()
    def __str__(self): #print function calls this
        return self.title

class Post(models.Model):
    class_name = models.CharField( max_length = 200, unique = True)
    credits = models.PositiveSmallIntegerField()
    student = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True)
    #student = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user', )
    def __str__(self): #print function calls this
        return self.class_name

class New(models.Model):
    filler = models.CharField( max_length = 200, unique = True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(max_length = 100, default = '')
    city = models.CharField(max_length = 100, default = '')
    phone = models.PositiveSmallIntegerField(default = 0)

    def __str__(self):
        return self.user.username

def create_profile(sender, **kwargs):
    if kwargs['created']: #if user has been created
        user_profile = UserProfile.objects.create(user = kwargs['instance']) #current user object
post_save.connect(create_profile, sender = User)