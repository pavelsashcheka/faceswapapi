from django.db import models


class User(models.Model):
    name = models.CharField(max_length=64, blank=False)
    surname = models.CharField(max_length=64, blank=False)
    birthdate = models.DateField(blank=False)
    school = models.CharField(max_length=256, blank=False)
    email = models.EmailField(blank=False, unique=True)


class ImageProcessing(models.Model):
    email = models.ForeignKey(User, on_delete=models.PROTECT, to_field='email', blank=False, null=True)
    background = models.CharField(max_length=64, blank=False)
    image = models.ImageField(blank=False, upload_to="pictures/sources")
    result_image = models.ImageField(blank=True, upload_to="pictures/results")
    result_image_string = models.TextField(blank=True)

