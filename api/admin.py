from . import models
from django.contrib import admin

# Register your models here.
admin.site.register(models.ActionVersion)
admin.site.register(models.Audio)
admin.site.register(models.AudioMeta)
admin.site.register(models.UserFreeTextTaskAnswers)
admin.site.register(models.NoVoiceRecognitionModel)
