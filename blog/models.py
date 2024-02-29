from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Posts(models.Model):
    user = models.ForeignKey(User,on_delete = models.SET_NULL, null=True , blank = True)
    post_id =  models.AutoField(primary_key=True)
    post_title = models.CharField(max_length=100)
    post_content = models.TextField()
    post_keywords = models.CharField(max_length=255)
    post_meta_tag = models.CharField(max_length=255)
    post_liked = models.ManyToManyField(User, related_name="post_likes",default=[0]
                                        ,blank=True)
    # img_src = models.TextField(null = True,blank=True)
    img_src = models.URLField(null = True, blank = True)
    alt_text = models.CharField(max_length= 255, null = True, blank= True)
    
    pub_date = models.DateTimeField()
    author = models.CharField(max_length=100)

    def total_likes(self):
        return self.post_liked.count()

    def __str__(self) -> str:
        return f"{str(self.post_id)}. {self.post_title}"