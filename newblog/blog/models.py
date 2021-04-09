from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.


class Author(models.Model):
    name = models.ForeignKey(User,on_delete=models.CASCADE)
    detail = models.CharField(max_length=200,null=True,blank=True)
    profile_pic = models.ImageField(upload_to = 'user_images/',blank=True,null=True)

    def __str__(self):
        return str(self.name)


class Category(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.name



class Article(models.Model):
    title = models.CharField(max_length=500,blank=True,null=True)
    post_author = models.ForeignKey(Author,on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True,blank=True)
    text = RichTextField(blank=True,null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
    image = models.ImageField(upload_to='images/',blank=True,null=True,default='images/nature.jpg')


    def __str__(self):
        return self.title








    