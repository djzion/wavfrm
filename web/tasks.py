import os, urllib
from celery.decorators import task
from audioprocessing.processing import convert_to_pcm, create_wave_images
from django.conf import settings
from django.core.files import File
from django.utils import simplejson

HEX = '0123456789abcdef'

def rgb(triplet):
    triplet = triplet.lower()
    return (HEX.index(triplet[0])*16 + HEX.index(triplet[1]),
            HEX.index(triplet[2])*16 + HEX.index(triplet[3]),
            HEX.index(triplet[4])*16 + HEX.index(triplet[5]))

def triplet(rgb):
    return hex(rgb[0])[2:] + hex(rgb[1])[2:] + hex(rgb[2])[2:]

@task()
def create_waveform(waveform):
    print("Executing task id %r, args: %r kwargs: %r" % (
        create_waveform.request.id, create_waveform.request.args, create_waveform.request.kwargs))
    
    track_ext = os.path.splitext(waveform.track.url)
    #We save the original compressed audio to a place where we wont have to redownload it
    track_tmp_file = os.path.join(settings.MEDIA_ROOT, 'track_tmp', '%d%s' % (waveform.id, track_ext[1]))
    track_tmp_wavfile = os.path.join(settings.MEDIA_ROOT, 'track_tmp', '%d.wav' % (waveform.id))
    
    if not os.path.exists(track_tmp_file):
        print 'Downloading %s to %s' % (waveform.track.url, track_tmp_file)
        urllib.urlretrieve(waveform.track.url, track_tmp_file)
        
    convert_to_pcm(track_tmp_file, track_tmp_wavfile)
    waveform_img = os.path.join(settings.TMP_DIR,  '%s_w.png' % str(waveform.id))
    spectrum_img = os.path.join(settings.TMP_DIR, '%s_s.jpg' % str(waveform.id))
    peaks = create_wave_images(track_tmp_wavfile, waveform_img, spectrum_img , 2048, 511, 2048, color=rgb(waveform.color), bgcolor=rgb(waveform.bgcolor))
    waveform.waveform_img.save('%s_w.png' % str(waveform.id), File(open(waveform_img)))
    waveform.spectrum_img.save('%s_w.png' % str(waveform.id), File(open(spectrum_img)))
    waveform.track.peaks = simplejson.dumps(peaks)
    waveform.save()
    waveform.track.save()
    
    #os.unlink(track_tmp_file)
    os.unlink(track_tmp_wavfile)
    return waveform