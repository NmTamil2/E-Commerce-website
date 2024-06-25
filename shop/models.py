from django.db import models
import datetime
import os

def getFileName(instance,filename):
    now_time = datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    new_filename = "%s%s"%(now_time,filename)
    return os.path.join('uploads/',new_filename)

class Category(models.Model):
    name = models.CharField(max_length=150, blank=False, null=False)
    image = models.ImageField(upload_to = getFileName,blank=True, null=True)
    description = models.TextField(max_length=1500, blank=False, null=False)
    status = models.BooleanField(default=False, help_text="0-show, 1-Hideen")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=150, blank=False, null=False)
    vendor = models.CharField(max_length=150, blank=False, null=False)
    product_image = models.ImageField(upload_to = getFileName,blank=True, null=True)
    quantity=models.IntegerField(null=False,blank=False)
    original_price = models.FloatField(null=False, blank=False)
    selling_price = models.FloatField(null=False, blank=False)
    description = models.TextField(max_length=1500, blank=False, null=False)
    status = models.BooleanField(default=False, help_text="0-show, 1-Hideen")
    Trending = models.BooleanField(default=False, help_text="0-default, 1-Trending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"


