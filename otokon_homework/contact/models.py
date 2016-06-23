from __future__ import unicode_literals
from django.db import models
from django.template.defaultfilters import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver
from homework.models import Homework
from django.contrib.auth.models import User


class Message(models.Model):
    send_user = models.ForeignKey(User, related_name="Send")
    to_user = models.ForeignKey(User, related_name="Take")
    homework = models.ForeignKey(Homework)
    title = models.CharField(max_length=100)
    content = models.TextField()
    is_answered = models.BooleanField(default=False)
    slug = models.SlugField(max_length=100)
    added_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


@receiver(pre_save,sender=Message)
def message_slug_handler(sender,instance,*args,**kwargs):
    instance.slug = slugify(instance.title)
