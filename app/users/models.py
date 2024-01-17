from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    def save(self, *args, **kwargs):
        super(CustomUser, self).save(*args, **kwargs)

    def str(self):
        return self.email or self.username


class Feedback(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE,
                             related_name='feedbacks')
    full_name = models.CharField(max_length=128, null=True, blank=True)
    comment = models.TextField(null=False, blank=False)


class Contact(models.Model):
    email = models.EmailField(max_length=254, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
