from django.db import models
from django.contrib.auth.models import  AbstractUser
# Create your models here.
# class UserProfile(models.Model):
#     user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='userprofile',primary_key=True)
#     profile_image = models.ImageField(upload_to='profile_images/',blank=True,null= True)
#     bio = models.TextField(blank=True)

#     def __str__(self):
#         return f'{self.user.username} profile'

    
class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images',blank=True, default='profile_images/default_image.jpg')
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username
      
