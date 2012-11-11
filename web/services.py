import json, pickle
from pyechonest.track import *
from pyechonest import config
from pyechonest.util import EchoNestAPIError
from decorators import timed
import os, urllib, numpy, wave, json, logging
from celery.decorators import task
from audioprocessing.processing import convert_to_pcm, create_wave_images
from django.conf import settings
from django.core.files import File
from audioprocessing.processing import AudioProcessor, WaveformImage
from decorators import timed
from drawing import rgb
from models import Waveform, WaveformStatus

config.ECHO_NEST_API_KEY="QGSW4XPT3YCHCIE61"

log = logging.getLogger(__name__)
peaks_per_second = 1
width = 2048
delete_mp3s = False
delete_wavs = True

@timed
def get_peaks(waveform, force_regen):
    track_ext = os.path.splitext(waveform.track.url)
    #We save the original compressed audio to a place where we wont have to redownload it
    track_tmp_file = os.path.join(settings.MEDIA_ROOT, 'track_tmp', '%d%s' % (waveform.id, track_ext[1]))
    track_tmp_wavfile = os.path.join(settings.MEDIA_ROOT, 'track_tmp', '%d.wav' % (waveform.id))

    if not os.path.exists(track_tmp_file) or force_regen:
        download_original(waveform, track_tmp_file)
    if not track_ext in ('.wav', ):
        convert_to_pcm(track_tmp_file, track_tmp_wavfile)
    processor = AudioProcessor(track_tmp_wavfile, width, numpy.hanning)

    wav = wave.open(track_tmp_wavfile)
    duration = wav.getnframes() / wav.getframerate()
    segments = duration * peaks_per_second
    samples_per_pixel = processor.audio_file.nframes / float(width)

    all_peaks = []
    all_centroids = []

    for x in range(width):
        seek_point = int(x * samples_per_pixel)
        next_seek_point = int((x + 1) * samples_per_pixel)
        all_peaks.append(processor.peaks(seek_point, next_seek_point))
        all_centroids.append(processor.spectral_centroid(seek_point)[0])

    waveform.track.duration = duration
    waveform.track.peaks = json.dumps(all_peaks)
    waveform.track.centroids = json.dumps(all_centroids)
    waveform.track.save()
    waveform.save()
    if delete_mp3s: os.unlink(track_tmp_file)
    if delete_wavs: os.unlink(track_tmp_wavfile)

@timed
def draw_peaks(waveform):
    track_tmp_wavfile = os.path.join(settings.MEDIA_ROOT, 'track_tmp', '%d.wav' % (waveform.id))
    color = [rgb(waveform.color)]
    if waveform.color_centroid: color.append(rgb(waveform.color_centroid))
    waveform_img = WaveformImage(width, 511, palette=[], bgcolor=None, color=color)
    waveform_img_filename = os.path.join(settings.TMP_DIR,  '%s_w.png' % str(waveform.id))
    if os.path.exists(waveform_img_filename): os.unlink(waveform_img_filename)
    peaks = json.loads(waveform.track.peaks)
    centroids = json.loads(waveform.track.centroids)
    for i in range(width):
        segment = peaks[i]
        waveform_img.draw_peaks(i, peaks[i], centroids[i])
        #waveform.spectrum_img.save('%s_s.png' % str(waveform.id), File(open(spectrum_img)))
    waveform_img.save(waveform_img_filename)
    waveform.waveform_img.save(waveform_img_filename, File(open(waveform_img_filename)))
    return waveform

@timed
def download_original(waveform, local_path):
    waveform.status = WaveformStatus.downloading
    waveform.save()
    resp = urllib.urlretrieve(waveform.track.url, local_path)
    log.info('Downloaded %s to %s' % (waveform.track.url, local_path))

@timed
def get_echonest_data_for_track(track):
    try:
        echo_track = track_from_url(track.url)
    except EchoNestAPIError:
        log.exception('Echonest failure for track %s' % track)
        return track

    track.title = echo_track.artist + ' - ' + echo_track.title
    track.echonest_analysis = json.dumps(echo_track.__dict__)
    track.save()
    return track