from django.db import models
from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from django.contrib.auth.models import User
from .models import Waveform, Track

class WaveformAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        if request.user and request.user.is_authenticated():
            return True

        return False

    # Optional but recommended
    def get_identifier(self, request):
        return request.user.username

class WaveformAuthorization(Authorization):
    def is_authorized(self, request, object=None):
        if object:
            if isinstance(object, Waveform) and object.track.user == request.user:
                return True
            elif isinstance(object, Track) and object.user == request.user:
                return True
            elif isinstance(object, User) and object == request.user:
                return True
            else:
                return False
        else:
            return True

    # Optional but useful for advanced limiting, such as per user.
    def apply_limits(self, request, object_list):
        return object_list

        #if request and hasattr(request, 'user'):
        #    return object_list.filter(track__user=request.user)
        #return object_list.none()

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        authentication = WaveformAuthentication()
        authorization = WaveformAuthorization()
        excludes = ('password', )

class MeAuthorization(WaveformAuthorization):

    def apply_limits(self, request, object_list):
        return object_list.filter(id=request.user.id)

class MeResource(UserResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'me'
        authentication = WaveformAuthentication()
        authorization = MeAuthorization()

class TrackResource(ModelResource):
    user = fields.ToOneField(UserResource, 'user', full = True, null=True)

    class Meta:
        queryset = Track.objects.all()
        resource_name = 'track'
        authentication = WaveformAuthentication()
        authorization = WaveformAuthorization()
        #excludes = ('centroids', 'peaks', 'echonest_analysis')

    def alter_list_data_to_serialize( self, request, data):
        if not request.REQUEST.get('full'):
            for item in data['objects']:
                item.data['echonest_analysis'] = None
                item.data['centroids'] = None
                item.data['peaks'] = None
        return data

    def alter_detail_data_to_serialize( self, request, data):
        if not request.REQUEST.get('full'):
            data.data['echonest_analysis'] = None
            data.data['centroids'] = None
            data.data['peaks'] = None
        return data

class WaveformResource(ModelResource):
    class Meta:
        queryset = Waveform.objects.all()
        resource_name = 'waveform'
        authentication = WaveformAuthentication()
        authorization = WaveformAuthorization()
