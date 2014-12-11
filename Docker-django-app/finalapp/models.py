from django.db import models
from django.contrib.auth.models import User

class Container(models.Model):
    uid=models.CharField(max_length=200)
    name_image=models.CharField(max_length=200)
    id_container=models.CharField(max_length=200)
    created = models.CharField(max_length=200)
    os = models.CharField(max_length=200)
    virual_size = models.CharField(max_length=200)

class Image(models.Model):
    uid=models.CharField(max_length=200)
    name=models.CharField(max_length=200)
    id_images=models.CharField(max_length=200)
    virtual_size = models.CharField(max_length=200)
    repo_tags = models.CharField(max_length=200)
    created = models.CharField(max_length=200)
    os = models.CharField(max_length=200)


class User_Image(models.Model):
    uid=models.CharField(max_length=200)
    name=models.CharField(max_length=200)
    id_images=models.CharField(max_length=200)
    virtual_size = models.CharField(max_length=200)
    repo_tags = models.CharField(max_length=200)
    created = models.CharField(max_length=200)
    os = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    cmd = models.CharField(max_length=200)

class pushed_images(models.Model):
    uid=models.CharField(max_length=200)
    name=models.CharField(max_length=200)
    id_images=models.CharField(max_length=200)
    virtual_size = models.CharField(max_length=200)
    repo_tags = models.CharField(max_length=200)
    created = models.CharField(max_length=200)
    os = models.CharField(max_length=200)


# Create your models here.