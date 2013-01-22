# -*- coding: utf-8 -*-
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from apps.file_uploader import qqFileUploader


@csrf_exempt
def upload(request):
    allowedExtension = [".jpg", ".png", ".ico", ".*"]
    sizeLimit = 1024000
    uploader = qqFileUploader(allowedExtension, sizeLimit)
    return HttpResponse(uploader.handleUpload(request, "/" + settings.MEDIA_ROOT + "/uploads/"))
