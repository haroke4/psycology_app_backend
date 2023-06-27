from django.contrib import admin
from django.urls import path, include
from . import views_auth, views, views_admin

urlpatterns = [
    # auth
    path('login', views_auth.Login.as_view()),
    path('is_token_valid', views_auth.IsTokenValid.as_view()),

    # main
    path('actions', views.GetActions.as_view()),

    path('audio_list', views.AudioList.as_view()),
    path('check_audio_meta', views.CheckAudioMeta.as_view()),
    path('create_user_free_text_task', views.CreateFreeTextTaskAnswer.as_view()),
    path('get_audio_file/<int:id>', views.GetAudio.as_view()),

    # for admins
    path('add_audio', views_admin.AddAudioView.as_view()),
    path('add_sheet', views_admin.UploadSheetView.as_view())
]