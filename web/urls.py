from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('web.views',
    (r'^$', 'homepage'),
    (r'^player/(?P<waveform_id>\d+)/$', 'player'),
    (r'^canvas_player/(?P<track_id>\d+)/$', 'canvas_track'),
    (r'^create_track/$', 'create_track'),
    (r'^waveform/$', 'create_waveform', {'respond_with': 'json'}),
    (r'^waveform/img/$', 'create_waveform', {'respond_with': 'img'}),
    (r'^waveform/(?P<waveform_id>\d+)/img/$', 'show_waveform_img'),
    (r'^waveform/(?P<waveform_id>\d+)/$', 'get_waveform'),
    (r'^track/(?P<track_id>\d+)/$', 'get_track'),
    (r'^user/tracks/$', 'user_tracks'),
    #(r'^accounts/login/$', 'django.contrib.auth.views.login'),
)