import hashlib
import os
import uuid

from os.path import join
from datetime import datetime

import mimetypes

from django.conf import settings as django_settings
from django.db import models
from django.template.defaultfilters import slugify
from django.core.files.images import get_image_dimensions
from django.utils.translation import ugettext_lazy as _

from django.contrib.contenttypes.models import ContentType

from unidecode import unidecode

try:
    from django.contrib.contenttypes.fields import GenericForeignKey
except ImportError:
    from django.contrib.contenttypes.generic import GenericForeignKey

from adminfiles import settings

if 'tagging' in django_settings.INSTALLED_APPS:
    from tagging.fields import TagField
else:
    TagField = None


def get_photo_path(instance, filename):
    """
    Function is dealing need for parameter `upload_to`.
    Puts image in MEDIA_ROOT/tour_images/ab/c0/abc01234567890123456789012345678.jpg
    """
    basename, ext = os.path.splitext(filename)
    hashed_name = hashlib.md5('{0}{1}{2}'.format(uuid.uuid4(), filename, datetime.now()).encode('utf-8')).hexdigest()
    return join(settings.ADMINFILES_UPLOAD_TO, hashed_name[:2], hashed_name[2:4], hashed_name + ext)


class FileUpload(models.Model):
    upload_date = models.DateTimeField(_('upload date'), auto_now_add=True)
    upload = models.FileField(_('file'), upload_to=get_photo_path)
    title = models.CharField(_('title'), max_length=100)
    form_field = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(_('slug'), max_length=100, unique=True)
    description = models.CharField(_('description'), blank=True, max_length=200)
    content_type = models.CharField(editable=False, max_length=100)
    sub_type = models.CharField(editable=False, max_length=100)

    if TagField:
        tags = TagField(_('tags'))
    
    class Meta:
        ordering = ['upload_date', 'title']
        verbose_name = _('file upload')
        verbose_name_plural = _('file uploads')

    def __unicode__(self):
        return self.title

    def mime_type(self):
        return '%s/%s' % (self.content_type, self.sub_type)
    mime_type.short_description = _('mime type')

    def type_slug(self):
        return slugify(self.sub_type)

    def is_image(self):
        return self.content_type == 'image'

    def _get_dimensions(self):
        try:
            return self._dimensions_cache
        except AttributeError:
            if self.is_image():
                self._dimensions_cache = get_image_dimensions(self.upload.path)
            else:
                self._dimensions_cache = (None, None)
        return self._dimensions_cache
    
    def width(self):
        return self._get_dimensions()[0]
    
    def height(self):
        return self._get_dimensions()[1]
    
    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            slug = slugify(unidecode(self.title))
            slug_exists = True
            counter = 1
            self.slug = slug
            while slug_exists:
                try:
                    slug_exits = FileUpload.objects.get(slug=slug)
                    if slug_exits:
                        slug = self.slug + '_' + str(counter)
                        counter += 1
                except FileUpload.DoesNotExist:
                    self.slug = slug
                    break
        try:
            uri = self.upload.path
        except NotImplementedError:
            uri = self.upload.url
        (mime_type, encoding) = mimetypes.guess_type(uri)
        try:
            [self.content_type, self.sub_type] = mime_type.split('/')
        except:
            self.content_type = 'text'
            self.sub_type = 'plain'
        super(FileUpload, self).save()

    def insert_links(self):
        links = []
        for key in [self.mime_type(), self.content_type, '']:
            if key in settings.ADMINFILES_INSERT_LINKS:
                links = settings.ADMINFILES_INSERT_LINKS[key]
                break
        for link in links:
            ref = self.slug
            opts = ':'.join(['%s=%s' % (k,v) for k,v in link[1].items()])
            if opts:
                ref += ':' + opts
            yield {'desc': link[0],
                   'ref': ref}

    def mime_image(self):
        if not settings.ADMINFILES_STDICON_SET:
            return None
        return ('http://www.stdicon.com/%s/%s?size=64'
                % (settings.ADMINFILES_STDICON_SET, self.mime_type()))

    @property
    def get_image_url(self):
        """ Return MEDIA_URL + self.photo """
        return join(settings.MEDIA_URL, str(self.upload)) if self.upload else ''



class FileUploadReference(models.Model):
    """
    Tracks which ``FileUpload``s are referenced by which content models.

    """
    upload = models.ForeignKey(FileUpload)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = ('upload', 'content_type', 'object_id')
