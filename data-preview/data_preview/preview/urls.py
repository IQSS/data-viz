from django.conf.urls import patterns, include, url


urlpatterns = patterns('preview.views',

    url(r'^hello/$', 'view_hello', name='view_hello_default'),

    url(r'^hello/(?P<name>\w{1,50})/$', 'view_hello', name='view_hello'),

)


