from django import forms
from django.http import HttpResponse
from django.contrib import admin

from adminsortable2.admin import SortableInlineAdminMixin

from adminfiles.models import FileUpload, Gallery, ImageForGallery
from adminfiles.settings import JQUERY_URL
from adminfiles.listeners import register_listeners


class FileUploadAdminForm(forms.ModelForm):

    model = FileUpload

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['form_field'].widget = forms.HiddenInput()


class FileUploadAdmin(admin.ModelAdmin):

    form = FileUploadAdminForm
    list_display = ['title', 'description', 'form_field', 'upload_date', 'upload', 'mime_type']
    list_editable = ['description']
    exclude = ('slug',)
# uncomment for snipshot photo editing feature
#    class Media:
#        js = (JQUERY_URL, 'photo-edit.js')
    def response_change(self, request, obj):
        if "_popup" in request.POST:
            return HttpResponse(
                '<script type="text/javascript">'
                'opener.dismissEditPopup(window);</script>')
        return super().response_change(request, obj)

    def delete_view(self, request, *args, **kwargs):
        response = super().delete_view(request, *args, **kwargs)
        if "post" in request.POST and "_popup" in request.GET:
            return HttpResponse(
                '<script type="text/javascript">'
                'opener.dismissEditPopup(window);</script>')
        return response

    def response_add(self, request, *args, **kwargs):
        if '_popup' in request.POST:
            return HttpResponse(
                '<script type="text/javascript">'
                'opener.dismissAddUploadPopup(window);</script>')
        return super().response_add(request, *args, **kwargs)


class FilePickerAdmin(admin.ModelAdmin):

    adminfiles_fields = []
    gallery_fields = []

    def __init__(self, *args, **kwargs):
        super(FilePickerAdmin, self).__init__(*args, **kwargs)
        register_listeners(self.model, self.adminfiles_fields)

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(FilePickerAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in self.adminfiles_fields:
            try:
                field.widget.attrs['class'] += " adminfilespicker"
            except KeyError:
                field.widget.attrs['class'] = 'adminfilespicker'
        if db_field.name in self.gallery_fields:
            try:
                field.widget.attrs['class'] += " galleryfield"
            except KeyError:
                field.widget.attrs['class'] = 'galleryfield'
        return field

    class Media:
        js = [JQUERY_URL, 'adminfiles/model.js']


class GalleryImagesInline(SortableInlineAdminMixin, admin.TabularInline):

    model = ImageForGallery
    extra = 2
    fields = ('show_order', 'image', 'image_tag',)
    readonly_fields = ('image_tag',)


class GalleryAdminForm(forms.ModelForm):

    model = Gallery

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['form_field'].widget = forms.HiddenInput()


class GalleryAdmin(admin.ModelAdmin):

    form = FileUploadAdminForm
    list_display = ['title', 'description', 'form_field']
    exclude = ('slug',)
    inlines = [GalleryImagesInline]

    def response_change(self, request, obj):
        if "_popup" in request.POST:
            return HttpResponse(
                '<script type="text/javascript">'
                'opener.dismissEditPopup(window);</script>')
        return super().response_change(request, obj)

    def delete_view(self, request, *args, **kwargs):
        response = super().delete_view(request, *args, **kwargs)
        if "post" in request.POST and "_popup" in request.GET:
            return HttpResponse(
                '<script type="text/javascript">'
                'opener.dismissEditPopup(window);</script>')
        return response

    def response_add(self, request, *args, **kwargs):
        if '_popup' in request.POST:
            return HttpResponse(
                '<script type="text/javascript">'
                'opener.dismissAddUploadPopup(window);</script>')
        return super().response_add(request, *args, **kwargs)


admin.site.register(FileUpload, FileUploadAdmin)
admin.site.register(Gallery, GalleryAdmin)
