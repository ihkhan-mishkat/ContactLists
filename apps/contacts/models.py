from django.db import models
from django.conf import settings


class Contact(models.Model):
 

    name = models.TextField(
        max_length=50, help_text='Enter Name')
    email = models.TextField(
        max_length=50, help_text='Enter Email', blank=True)
    phone = models.CharField(
        max_length=20, help_text='Enter Phone', blank=True)
    address = models.TextField(
        max_length=300, help_text='Enter Address', blank=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.name[:50]
