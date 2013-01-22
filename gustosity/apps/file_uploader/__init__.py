"""
@author: Ferdinand E. Silva
@email: ferdinandsilva@ferdinandsilva.com
@website: http://ferdinandsilva.com
"""
import os
from django.conf import settings
from django.utils import simplejson as json
from django.core.files import File
from django.contrib.auth.models import User
from apps.recipe.models import Step, Recipe


class qqFileUploader(object):

    def __init__(self, allowedExtensions=None, sizeLimit=None):
        self.allowedExtensions = allowedExtensions or []
        self.sizeLimit = sizeLimit or settings.FILE_UPLOAD_MAX_MEMORY_SIZE

    def handleUpload(self, request, uploadDirectory):
        #read file info from stream
        uploaded = request.read
        #get file size
        fileSize = int(uploaded.im_self.META["CONTENT_LENGTH"])
        #get file name
        fileName = uploaded.im_self.META["HTTP_X_FILE_NAME"]
        #check first for allowed file extensions
        #read the file content, if it is not read when the request is multi part then the client get an error
        fileContent = uploaded(fileSize)
        if self._getExtensionFromFileName(fileName) in self.allowedExtensions or ".*" in self.allowedExtensions:
            #check file size
            if fileSize <= self.sizeLimit:
                #upload file & save
                fname = os.path.join(uploadDirectory, fileName)
                file = open(fname, "wb+")
                file.write(fileContent)
                file.close()
                # reload to create thumbs & other images
                uploaded_image = File(open(fname, "r"))

                step = recipe = None
                # Check user
                user_slug = request.GET.get('user', None)
                if user_slug is None or not User.objects.filter(username__iexact=user_slug).exists():
                    return json.dumps({"error": "Which user??."})

                # Check recipe and user permissions
                recipe_slug = request.GET.get('recipe', None)
                if recipe_slug is not None:
                    if not Recipe.objects.filter(slug=recipe_slug, user__username__iexact=user_slug).exists():
                        return json.dumps({"error": "This user doesn't have permissions to upload photos to this recipe."})
                    else:
                        recipe = Recipe.objects.get(slug=recipe_slug, user__username__iexact=user_slug)
                else:
                    return json.dumps({"error": "Which recipe??."})

                # Check step
                step_id = request.GET.get('step', None)
                if step_id is None:
                    return json.dumps({"error": "Which step??."})

                step = Step.objects.get(pk=step_id)
                step.original_image.save(fileName, uploaded_image)
                step.save()

                return json.dumps({
                    "success": True,
                    "thumb": step.thumbnail.url,
                    "id": step.pk,
                    })

                return json.dumps({"error": "Undefined error."})

            else:
                return json.dumps({"error": "File is too large."})
        else:
            return json.dumps({"error": "File has an invalid extension."})

    def _getExtensionFromFileName(self, fileName):
        filename, extension = os.path.splitext(fileName)
        return extension.lower()
