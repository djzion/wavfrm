import json
from django.shortcuts import get_object_or_404, get_list_or_404, render_to_response
from django.template.context import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.utils import simplejson
from django.core.serializers import serialize
from django.db.models import ObjectDoesNotExist
from django.conf import settings
from django.contrib.auth.decorators import login_required
from PIL import ImageFont, Image, ImageDraw
from web.tasks import create_waveform
from web.models import *

def homepage(request):
    return render_to_response('homepage.html', locals(), context_instance=RequestContext(request))

@login_required
def user_tracks(request):
    tracks = Track.objects.get(user=request.user).order_by('-created')
    return render_to_response('user/tracks.html', locals(), context_instance=RequestContext(request))

def player(request, track_id):
    tracks = get_list_or_404(Track, id=track_id)
    track = tracks[0]
    track_json = serialize('json', tracks)
    return render_to_response('player.html', locals(), context_instance=RequestContext(request))

def create_track(request):
    if request.method == 'POST':
        t = Track(
            url = request.REQUEST['url']
        )
        t.save()
        create_waveform(t)
        
    return render_to_response('create_track.html', locals(), context_instance=RequestContext(request))
    
def waveform(request):
    if 'bgcolor' in request.GET:
        bgcolor = request.GET['bgcolor']
    else:
        bgcolor = 'ffffff'
    
    if 'color' in request.GET:
        color = request.GET['color']
    else:
        color = '333333'
        
    if 'force_regen' in request.GET:
        force_regen = True
    else:
        force_regen = False
        
    if 'async' in request.GET:
        async = bool(int(request.GET['async']))
    else:
        async = True

    if 'track_id' in request.GET:
        try:
            track = Track.objects.get(id=request.GET['track_id'])
        except ObjectDoesNotExist:
            return HttpResponseNotFound()
            
    elif 'url' in request.GET:
        #find track for this url, or create one
        try:
            track = Track.objects.get(url=request.GET['url'])
        except ObjectDoesNotExist:
            track = Track(
                url = request.GET['url']
            )
            track.save()
            
    #find a waveform of matching params for this track, if it exists its image is created redirect to it
    try:
        waveform = track.waveform_set.get(bgcolor=bgcolor, color=color)
        #pdb.set_trace()
        if waveform.waveform_img and not force_regen:
            return HttpResponse(waveform.waveform_img.read(), mimetype='image/png')
    #else create one
    except ObjectDoesNotExist:
        waveform = Waveform(
            track = track,
            bgcolor = bgcolor,
            color = color
        )
        waveform.save()
    
    if async:
        create_waveform.delay(waveform)
        return waveform_processing(request, track)
    else:
        create_waveform(waveform)
        return HttpResponse(waveform.waveform_img.read(), mimetype='image/png')

def get_track(request, track_id):
    track = Track.objects.get(id=track_id)
    from django.core.serializers.json import DjangoJSONEncoder
    from django.core import serializers
    data = serializers.serialize("json", [track])
    return HttpResponse(data)

def canvas_track(request, track_id):
    return render_to_response('canvas_player.html', locals(), context_instance=RequestContext(request))
            
def waveform_processing(request, t):
    """
    Interstitial for async mode
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