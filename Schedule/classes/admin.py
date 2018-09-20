from django.contrib import admin

# Register your models here.
from .models import Course, UserProfile, Post

admin.site.register(Course)

admin.site.register(UserProfile)

admin.site.register(Post)