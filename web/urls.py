from django.conf.urls import patterns, include, url
from tastypie.api import Api
from api import WaveformResource, TrackResource, UserResource, MeResource

v1_api = Api(api_name='v1')
v1_api.register(TrackResource())
v1_api.register(WaveformResource())
v1_api.register(UserResource())
v1_api.register(MeResource())

urlpatterns = patterns('web.views',
    (r'^$', 'homepage'),
    (r'^recent-tracks/$', 'recent_tracks'),
    (r'^about/$', 'about'),
    (r'^player/(?P<waveform_id>\d+)/$', 'player'),
    (r'^canvas_player/(?P<track_id>\d+)/$', 'canvas_track'),

    (r'^api/', include(v1_api.urls)),

    (r'^waveform/$', 'create_waveform', {'respond_with': 'json'}),
    (r'^waveform/img/$', 'create_waveform', {'respond_with': 'img'}),
    (r'^waveform/(?P<waveform_id>\d+)/img/$', 'show_waveform_img'),
    (r'^waveform/(?P<waveform_id>\d+)/$', 'get_waveform'),
    (r'^track/(?P<track_id>\d+)/$', 'get_track'),
    (r'^my/tracks/$', 'user_tracks'),
    (r'^(?P<username>\d+)/tracks/$', 'user_tracks'),
    #(r'^accounts/login/$', 'django.contrib.auth.views.login'),
)