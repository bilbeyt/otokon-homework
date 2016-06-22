from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class Lecture(models.Model):
    name = models.CharField(max_length=100)
    publish_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


def get_homework_detail_path(instance, filename):
    return "documents/details/{}/{}".format(instance.lecture, filename)

def get_answers_upload_path(instance, filename):
    return "documents/answers/{}/{}/{}".format(
                                    instance.homework, instance.user, filename)


class Homework(models.Model):
    lecture = models.ForeignKey(Lecture)
    number = models.PositiveSmallIntegerField()
    publish_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    document = models.FileField(upload_to=get_homework_detail_path)
    is_available = models.BooleanField(default=False)
    publish_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} {}".format(self.lecture, self.number)


class AnswerSheet(models.Model):
    user = models.ForeignKey(User)
    homework = models.ForeignKey(Homework,
                                limit_choices_to={"is_available" : True})
    comment = models.TextField()
    answers = models. FileField(upload_to=get_answers_upload_path)
    publish_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}-{}".format(self.user, self.homework)
