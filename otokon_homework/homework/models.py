from __future__ import unicode_literals
from django.db import models
from django.template.defaultfilters import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
import os


@python_2_unicode_compatible
class Lecture(models.Model):
    name = models.CharField(max_length=100)
    is_available = models.BooleanField(default=False)
    slug = models.SlugField(max_length=100,blank=True,null=True)
    publish_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


def get_homework_detail_path(instance, filename):
    return "documents/details/{}/{}".format(instance.lecture, filename)

def get_answers_upload_path(instance, filename):
    return "documents/answers/{}/{}/{}".format(
                                    instance.homework, instance.user, filename)


@python_2_unicode_compatible
class Homework(models.Model):
    lecture = models.ForeignKey(Lecture)
    number = models.PositiveSmallIntegerField()
    lecturer = models.ForeignKey(User)
    publish_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField(null=True, blank=True)
    document = models.FileField(upload_to=get_homework_detail_path)
    is_available = models.BooleanField(default=False)
    slug = models.SlugField(max_length=100,blank=True,null=True)
    publish_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} {}".format(self.lecture, self.number)

    def filename(self):
        return os.path.basename(self.document.name)


@python_2_unicode_compatible
class AnswerSheet(models.Model):
    user = models.ForeignKey(User)
    homework = models.ForeignKey(Homework,
                                limit_choices_to={"is_available" : True})
    comment = models.TextField(null=True, blank=True)
    answers = models. FileField(upload_to=get_answers_upload_path)
    slug = models.SlugField(max_length=100,blank=True,null=True)
    publish_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}-{}".format(self.user, self.homework)


@receiver(pre_save,sender=Lecture)
def lecture_slug_handler(sender,instance,*args,**kwargs):
    instance.slug = slugify(instance.name)

@receiver(pre_save,sender=Homework)
def homework_slug_handler(sender,instance,*args,**kwargs):
    title = "homework-{}".format(instance.number)
    instance.slug = slugify(title)

@receiver(pre_save,sender=AnswerSheet)
def answersheet_slug_handler(sender,instance,*args,**kwargs):
    instance.slug = slugify(instance.homework)
