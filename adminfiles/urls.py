from django.conf.urls import patterns, url

from django.contrib.admin.views.decorators import staff_member_required

from adminfiles.views import download, get_enabled_browsers

urlpatterns = [
    url(r'download/$', staff_member_required(download),
        name="adminfiles_download")
]

for browser in get_enabled_browsers():
    slug = browser.slug()
    urlpatterns += [
        url('%s/$' % slug, browser.as_view(),
            name='adminfiles_%s' % slug)
    ]