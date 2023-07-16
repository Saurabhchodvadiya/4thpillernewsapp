from django.db import models
from autoslug import AutoSlugField
from datetime import datetime
from embed_video.fields import EmbedVideoField
from ckeditor.fields import RichTextField

# Create your models here.


delete_choices= (
    ('deleted','deleted'),
    ('not deleted','not deleted'),

)


class  Main_category(models.Model):
    title=models.CharField(max_length=200,unique=True)
    delete_status = models.CharField(max_length=200, choices=delete_choices, default='not deleted')

    def __str__(self):
        return f'{self.title} '


class  Category(models.Model):
    main_category=models.ForeignKey(Main_category, on_delete=models.CASCADE,null=True,blank=True)
    title=models.CharField(max_length=200,unique=True)
    Image=models.ImageField(upload_to ='media/category',default="media/category/blank.png", null=True, blank=True)
    delete_status = models.CharField(max_length=200, choices=delete_choices, default='not deleted')

    def __str__(self):
        return f'{self.title} '
    

status_choices= (
    ('New','New'),
    ('Most Read','Most Read'),
    ('Trending','Trending')
)
front_choices= (
    ('Show','Show'),
    ('Dont Show','Dont Show'),

)

class latest_news(models.Model):
    category=models.ForeignKey(Category,null=True,blank=True, on_delete=models.SET_NULL)
    title=models.CharField(max_length=200)
    slug= AutoSlugField(populate_from='title',unique=True,null=True,default=None)
    status = models.CharField(max_length=200, choices=status_choices, default='New')
    show_front = models.CharField(max_length=200, choices=front_choices, default='Show')
    delete_status = models.CharField(max_length=200, choices=delete_choices, default='not deleted')
    author=models.CharField(max_length=200,null=True,blank=True)
    Image=models.ImageField(upload_to ='media/%Y/%m/%d/',null=True,blank=True)
    details=RichTextField(blank=True, null=True)
    image_2=models.ImageField(upload_to ='media/%Y/%m/%d/',null=True,blank=True)
    img2_details=RichTextField(blank=True, null=True)
    Image_3=models.ImageField(upload_to ='media/%Y/%m/%d/',null=True,blank=True)
    img3_details=RichTextField(blank=True, null=True)
    date=models.DateTimeField(default=datetime.today)
    # SEO input field.
    meta_title = models.CharField(max_length=120,null=True,blank=True)
    meta_description = models.CharField(max_length=120,null=True,blank=True)
    meta_keyword = models.CharField(max_length=255,null=True,blank=True)


    def __str__(self):
        return f'{self.slug} '



class Videos(models.Model):
    url=EmbedVideoField()
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.url} '


class Donation(models.Model):

    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100 ,null=True,blank=True)
    duration=models.CharField(max_length=10)
    amount=models.IntegerField(null=True,blank=True)
    email=models.EmailField(max_length=100)
    phone=models.CharField(max_length=15)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'