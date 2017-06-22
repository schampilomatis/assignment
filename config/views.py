# -*- coding: utf-8 -*-
from rest_framework.decorators import api_view
from django.http import HttpResponse
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from django.http import HttpResponseRedirect
from PIL import Image
import subprocess
from django.conf import settings
import os

@api_view(['GET'])
@permission_classes((AllowAny, ))
def get_models(request):
    
    download_param = request.GET.get('download')
    try:
        subprocess.call('python {}/manage.py graph_models -o {}/models.png'.format(settings.ROOT_DIR, settings.MEDIA_ROOT), shell=True)
    except Exception, e:
        print e
    if download_param:
        filename = 'models.png'
        path = settings.MEDIA_ROOT
        response = HttpResponse(content_type='image/png')
        im = Image.open(os.path.join(path, filename))
        response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
        im.save(response, 'png')
        return response
    else:
        filename = 'models.png'
    path = 'media/{}'.format(filename)
    response = HttpResponse('<html><body><img src="{}"></body></html>'.format(path),content_type='text/html')
    
    return response