from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
# Create your models here.
class post(models.Model):
    STATUS_CHOICES = (('draft','Draft'),('published','Published'))
    CATEGORY_CHOICES = (('travel blogs','Travel Blogs'),('fashion blogs','Fashion Blogs'),('food blogs','Food Blogs'),('educational blogs','Educational Blogs'),('parenting blogs','Parenting Blogs'),('movie and music blogs','Movie And Music Blogs'),('sports blogs','Sports Blogs'),('personal blogs','Personal Blogs'),('other','Other'))
    title = models.CharField(max_length = 260)
    slug = models.SlugField(max_length = 264,unique_for_date='publish')
    author = models.ForeignKey(User,related_name='blog_posts',on_delete=models.CASCADE)
    body = models.TextField()
    publish = models.DateTimeField(default = timezone.now)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now_add = True)
    image = models.FileField(upload_to = "images/",default="blogger.jpg")
    status = models.CharField(max_length = 20,choices = STATUS_CHOICES,default = 'draft')
    category = models.CharField(max_length = 50,choices = CATEGORY_CHOICES,default = 'other')
    def get_absolute_url(self):
        return reverse("allblogs")
    class Meta:
        ordering = ('-publish',)
    def __str__(self):
        return self.title

# model to save all the comments
class comment(models.Model):
    pst = models.ForeignKey(post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField(max_length = 160)
    comment_time = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return '{}-{}'.format(self.pst.title,str(self.user.username))

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    dob = models.DateField(null = True, blank = True)
    photo = models.ImageField(null = True,blank = True, default="avatar2.jpg")

    def __str__(self):
        return "profile of user {}".format(self.user.username)
