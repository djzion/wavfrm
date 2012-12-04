import json
from django.shortcuts import get_object_or_404, get_list_or_404, render_to_response
from django.template.context import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseForbidden
from django.core.serializers import serialize
from django.db.models import ObjectDoesNotExist
from django.conf import settings
from django.contrib.auth.decorators import login_required
from PIL import ImageFont, Image, ImageDraw
from .tasks import create_waveform_task
from .models import *
from .util import humanize_filename

def homepage(request):
    return render_to_response('homepage.html', locals(), context_instance=RequestContext(request))

def about(request):
    return render_to_response('about.html', locals(), context_instance=RequestContext(request))

def user_tracks(request, username=None):
    if username is None:
        if request.user and request.user.is_authenticated(): user = request.user
        else: return HttpResponseForbidden('please log in')
    else:
        user = get_object_or_404(User, username=username)
    tracks = Track.objects.filter(user=user).order_by('-created')
    return render_to_response('user/tracks.html', locals(), context_instance=RequestContext(request))

def recent_tracks(request):
    tracks = Track.objects.all().order_by('-created')[:8]
    return render_to_response('recent_tracks.html', locals(), context_instance=RequestContext(request))

def player(request, waveform_id):
    waveform = get_object_or_404(Waveform, id=waveform_id)
    track = waveform.track
    track_json = serialize('json', [track])
    return render_to_response('player.html', locals(), context_instance=RequestContext(request))

def create_waveform(request, respond_with='img'):
    async = int(request.REQUEST.get('async', 1))
    force_regen = int(request.REQUEST.get('force_regen', 0))

    wave_params = {'color': '006699', 'color_centroid': '52d3d3'}
    if 'bgcolor' in request.REQUEST and request.REQUEST['bgcolor'] != '': wave_params['bgcolor'] = request.REQUEST['bgcolor']
    if 'color' in request.REQUEST and request.REQUEST['color'] != '': wave_params['color'] = request.REQUEST['color']
    if 'color_centroid' in request.REQUEST and request.REQUEST['color_centroid'] != '': wave_params['color_centroid'] = request.REQUEST['color_centroid']

    if 'track_id' in request.REQUEST:
        try:
            track = Track.objects.get(id=request.REQUEST['track_id'])
        except Track.DoesNotExist:
            return HttpResponseNotFound()
            
    elif 'url' in request.REQUEST:
        #find track for this url, or create one
        try:
            track = Track.objects.get(url=request.REQUEST['url'])
            existing_track = True
        except Track.DoesNotExist:
            existing_track = False
            track = Track(url = request.REQUEST['url'])
            track.title = humanize_filename(os.path.basename(request.REQUEST['url']))
            if request.user and request.user.is_authenticated(): track.user = request.user
            track.save()
            
    #find a waveform of matching params for this track, if it exists its image is created redirect to it
    try:
        waveform = track.waveform_set.get(**wave_params)
        if waveform.waveform_img and not force_regen:
            if respond_with == 'img': return HttpResponse(waveform.waveform_img.read(), mimetype='image/png')
            else: return get_waveform(request, waveform.id)
    #else create one
    except ObjectDoesNotExist:
        waveform = Waveform(**wave_params)
        waveform.track_id = track.id
        waveform.save()
    
    if not existing_track and async:
        create_waveform_task.delay(waveform, force_regen=force_regen)
        return HttpResponse(json.dumps({ 'track_id': track.id, 'waveform_id': waveform.id, 'status': waveform.status }))
    else:
        create_waveform_task(waveform, force_regen=force_regen)
        if respond_with == 'img': return HttpResponse(waveform.waveform_img.read(), mimetype='image/png')
        else: return get_waveform(request, waveform.id)

def show_waveform_img(request, waveform_id):
    waveform = get_object_or_404(Waveform, id=waveform_id)
    return HttpResponse(waveform.waveform_img.read(), mimetype='image/png')

def get_waveform(request, waveform_id):
    waveform = Waveform.objects.get(id=waveform_id)
    return HttpResponse(json.dumps({ 'track_id': waveform.track.id, 'waveform_id': waveform.id, 'status': waveform.status }))

def get_track(request, track_id):
    track = Track.objects.get(id=track_id)
    data = serialize("json", [track])
    return HttpResponse(data)

def canvas_track(request, track_id):
    return render_to_response('canvas_player.html', locals(), context_instance=RequestContext(request))

def waveform_processing(request):
    """
    Interstitial for synchronouts mode
    :param request:
    :param t:
    :return:
    """
    font = ImageFont.truetype(settings.PROJECT_PATH + '/web/static/fonts/Rockwell.ttf', 14)
    img=Image.new("RGBA", (200,100), None)
    draw = ImageDraw.Draw(img)
    draw.text((0, 0),"Waveform processing...",(50, 50, 50),font=font)
    draw = ImageDraw.Draw(img)
    draw = ImageDraw.Draw(img)
    response = HttpResponse(mimetype="image/png")
    img.save(response, "PNG")
    return response