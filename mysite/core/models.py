from atexit import register
from email.policy import default
import os
from django import template
from django.db import models
from django.contrib.auth.models import User


class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    file_name = models.CharField(max_length=100, null=True, blank=True)
    file_size = models.CharField(max_length=30, null=True, blank=True)
    page_count = models.IntegerField(null=True,blank=True)
    title = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='files/pdfs/')
    first_name=models.CharField(max_length=100,default="")
    last_name=models.CharField(max_length=100,default="")
    email=models.EmailField(default="")
   
    

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.pdf.delete()
        super().delete(*args, **kwargs)



