from tastypie.resources import ModelResource
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from .models import Waveform

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
            else:
                return False
        else:
            return True

    # Optional but useful for advanced limiting, such as per user.
    def apply_limits(self, request, object_list):
        return object_list

        if request and hasattr(request, 'user'):
            return object_list.filter(track__user=request.user)

        return object_list.none()

class WaveformResource(ModelResource):
    class Meta:
        queryset = Waveform.objects.all()
        resource_name = 'waveform'
        authentication = WaveformAuthentication()
        authorization = WaveformAuthorization()