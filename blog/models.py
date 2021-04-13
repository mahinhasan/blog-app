from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save

# Create your models here.


class Author(models.Model):
    name = models.ForeignKey(User,on_delete=models.CASCADE)
    detail = models.CharField(max_length=200,null=True,blank=True)
    profile_pic = models.ImageField(upload_to = 'user_images/',blank=True,null=True)

    def __str__(self):
        return str(self.name)


def create_profile(sender,**kwargs):
    if kwargs['created']:
        profile = Author.objects.create(name=kwargs['instance'])


class Category(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.name



class Article(models.Model):
    title = models.CharField(max_length=500,blank=True,null=True)
    post_author = models.ForeignKey(Author,on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True,blank=True)
    text = RichTextField(blank=True,null=True)
    likes = models.ManyToManyField(User,related_name='likes',null=True,blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True,default="Anything")
    image = models.ImageField(upload_to='images/',blank=True,null=True,default='images/nature.jpg')


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail', args=[self.id])
    
    def total_likes(self):
        return self.likes.count()


class Comment(models.Model):
    post = models.ForeignKey(Article,on_delete=models.CASCADE)
    name = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.TextField()
    cmnt_time = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey('Comment',on_delete=models.CASCADE,null=True,related_name='replies')

    def __str__(self):
        return self.post.title





    