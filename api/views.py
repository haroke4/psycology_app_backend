import json

from django.http import FileResponse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api import models

UP_TO_DATE = 'Up to date'


def error_with_text(text):
    return Response({'message': text}, status=status.HTTP_400_BAD_REQUEST)


def success_with_text(text, s=status.HTTP_200_OK):
    return Response({'message': text}, status=s)


def up_to_date():
    return success_with_text(UP_TO_DATE, s=status.HTTP_202_ACCEPTED)


class GetActions(APIView):
    def get(self, request: Request, *args, **kwargs):
        last_version = models.ActionVersion.objects.first().version_number
        with open('files/data.json', 'r') as f:
            data = {'version': last_version, 'actions': json.load(f)}
        return success_with_text(data)

    def post(self, request: Request):
        version = request.data.get('version')
        if version is None:
            return error_with_text('provide version')

        last_version = models.ActionVersion.objects.first().version_number
        if last_version == version:
            return up_to_date()

        return success_with_text('Please update your data by requesting GET request to this url')


class AudioList(APIView):
    def get(self, request: Request, *args, **kwargs):
        """
        Get list of audio data
        :param request:
        :return:
        """

        data = [i.to_dict() for i in models.Audio.objects.all()]

        audio_meta_data = models.AudioMeta.objects.first()
        data = {'audio_meta_version': audio_meta_data.version_number,
                'data': data}

        return success_with_text(data)

    def post(self, request: Request, *args, **kwargs):
        """
        Check audio list that user gives, and decide whether update or not
        :param request:
        :return:
        """
        data = request.data

        try:
            # data = {"audio_id": audio_version}
            # почему то в джейсоне ключом не может быть цифра в flutter

            update_list = []  # List of audio ID that user need to update (download)

            for servers_audio in models.Audio.objects.all():
                users_audio_version = data.get(str(servers_audio.id))
                if users_audio_version != servers_audio.version_number:
                    update_list.append(servers_audio.to_dict())

            return success_with_text(update_list)

        except KeyError as e:
            return error_with_text(e)


class CheckAudioMeta(APIView):
    def post(self, request: Request, *args, **kwargs):
        data = request.data

        try:
            # data = {'count_of_audios': int, 'audio_meta_version': int}
            audio_meta_data = models.AudioMeta.objects.first()

            if audio_meta_data.version_number == data['version']:
                return up_to_date()

            return success_with_text('You are not up to date')

        except Exception as e:
            return error_with_text(e)


class GetAudio(APIView):
    def get(self, request: Request, *args, **kwargs):
        id_ = kwargs.get('id')

        if id_ is None:
            return error_with_text('Provide id of audio')

        audio = models.Audio.objects.filter(id=id_).first()
        if audio is None:
            return error_with_text('No audio with this id')

        return FileResponse(open(audio.path_to_file, 'rb'), content_type='m4a')


class CreateFreeTextTaskAnswer(APIView):
    def post(self, request: Request, *args, **kwargs):
        user = request.user
        text = request.data.get('text')
        task_id = request.data.get('task_id')

        if not text:
            return error_with_text('no text')

        if not task_id:
            return error_with_text('no task id')

        model = models.UserFreeTextTaskAnswers()
        model.user = user
        model.text = text
        model.task_id = task_id
        model.save()

        return success_with_text(True)


class GetNoVoiceRecognitionModel(APIView):
    def post(self, request: Request, *args, **kwargs):
        return success_with_text([i.task_id for i in models.NoVoiceRecognitionModel.objects.all()])
