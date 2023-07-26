from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class ActionVersion(models.Model):
    version_number = models.IntegerField(default=0)
    changed_date = models.DateTimeField(default=timezone.now)

    def new_version(self):
        self.version_number += 1
        self.changed_date = timezone.now()
        self.save()


class Audio(models.Model):
    version_number = models.IntegerField(default=1)
    name = models.CharField(max_length=200, null=False, blank=False)
    path_to_file = models.CharField(max_length=200, null=False, blank=False)
    changed_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def to_dict(self):
        return {'id': self.id, 'version': self.version_number, 'name': self.name}

    def new_version(self):
        self.version_number += 1
        self.changed_date = timezone.now()
        self.save()


class AudioMeta(models.Model):
    version_number = models.IntegerField(default=0)
    changed_date = models.DateTimeField(default=timezone.now)

    def new_version(self):
        self.version_number += 1
        self.changed_date = timezone.now()
        self.save()


class UserFreeTextTaskAnswers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_free_text_task_answers')
    task_id = models.CharField(max_length=100)
    text = models.CharField(max_length=99999)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} {self.created_date.date()} {self.created_date.hour}:{self.created_date.minute}'


class NoVoiceRecognitionModel(models.Model):
    task_id = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.task_id} {self.created_date}'
