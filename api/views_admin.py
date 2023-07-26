from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.core.files.uploadedfile import InMemoryUploadedFile

from api import models

from .forms import *
from .parse_sheet import parseSheetAndSaveAsJson


#
class AddAudioView(FormView):
    form_class = MultiFileFieldForm
    template_name = "upload_audios.html"  # Replace with your template.
    success_url = "/admin"  # Replace with your URL or reverse().

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_staff:
            context = self.get_context_data()
            context['files'] = [i.to_dict() for i in models.Audio.objects.all()]
            return self.render_to_response(context)
        return redirect('/admin/login')

    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('/admin/login')

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        files = form.cleaned_data["file_field"]
        for f in files:
            f: InMemoryUploadedFile

            with open(f'files/audio_files/{f.name}', 'wb') as file:
                file.write(f.read())

            audio = models.Audio.objects.filter(name=f.name).first()
            if audio is None:
                audio = models.Audio()
                audio.name = f.name
            audio.new_version()
            audio.path_to_file = f'files/audio_files/{f.name}'
            audio.save()

        audio_meta = models.AudioMeta.objects.first()
        audio_meta.new_version()

        return HttpResponse('Audio files uploaded successfully')


# sheet
class UploadSheetView(FormView):
    form_class = UploadSheetForm
    template_name = "upload_sheet.html"  # Replace with your template.

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_staff:
            return super().get(request, *args, **kwargs)
        return redirect('/admin/login')

    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('/admin/login')

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        file = form.cleaned_data['file']
        cell_range_start = form.cleaned_data['cell_range_start']
        cell_range_stop = form.cleaned_data['cell_range_stop']

        with open('files/data.xlsx', 'wb') as f:
            f.write(file.read())

        try:
            parseSheetAndSaveAsJson(cell_range_start, cell_range_stop)
            a = models.ActionVersion.objects.first()
            a.new_version()

            return HttpResponse('Sheet uploaded successfully!')

        except Exception as e:
            return HttpResponse(f'Invalid cell ranges. Python error: {e}')
