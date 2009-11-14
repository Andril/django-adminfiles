from os.path import join
from django.conf import settings

JQUERY_URL = getattr(
    settings, 'JQUERY_URL',
    'http://ajax.googleapis.com/ajax/libs/jquery/1.3/jquery.min.js')

UPLOAD_MEDIA_URL = getattr(settings, 'UPLOAD_MEDIA_URL', settings.MEDIA_URL)

UPLOAD_RELATIVE_PATH = getattr(settings, 'UPLOAD_RELATIVE_PATH', 'uploads')

UPLOAD_THUMB_ORDERING = getattr(settings, 'UPLOAD_THUMB_ORDERING', ('-upload_date',))

FLICKR_USER = getattr(settings, 'FLICKR_USER', None)
FLICKR_API_KEY = getattr(settings, 'FLICKR_API_KEY', None)
YOU_TUBE_USER = getattr(settings, 'YOU_TUBE_USER', None)
