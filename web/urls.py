from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('web.views',
    (r'^$', 'homepage'),
    (r'^player/(?P<track_id>\d+)/$', 'player'),
    (r'^create_track/$', 'create_track'),
    (r'^waveform/$', 'waveform'),
    (r'^user/tracks/$', 'user_tracks'),
    #(r'^accounts/login/$', 'django.contrib.auth.views.login'),
)