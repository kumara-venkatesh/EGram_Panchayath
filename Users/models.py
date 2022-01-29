from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    profile_pic = models.ImageField(default='default.jpg', upload_to='profile_pics/')
    BirthDate = models.DateField()
    phoneno = models.CharField(max_length=10)
    address = models.CharField(max_length=200)
    Qualification = models.CharField(max_length=100, blank=True, default=None, null=True)
    Department = models.CharField(max_length=50)

    def __str__(self):
        return self.user.first_name + ' Profile'

    def save(self, **kwargs):
        super().save()

        image = Image.open(self.profile_pic.path)

        if image.width > 300 and image.height > 300:
            output_size = (300, 300)
            image.thumbnail(output_size)
            image.save(self.img.path)
