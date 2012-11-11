import os, urllib, numpy, wave, json, logging
from celery.decorators import task
from audioprocessing.processing import convert_to_pcm, create_wave_images
from django.conf import settings
from django.core.files import File
from audioprocessing.processing import AudioProcessor, WaveformImage
from decorators import timed
from drawing import rgb

log = logging.getLogger(__name__)
peaks_per_second = 1
width = 2048

@timed
def get_peaks(waveform):
    track_ext = os.path.splitext(waveform.track.url)
    #We save the original compressed audio to a place where we wont have to redownload it
    track_tmp_file = os.path.join(settings.MEDIA_ROOT, 'track_tmp', '%d%s' % (waveform.id, track_ext[1]))
    track_tmp_wavfile = os.path.join(settings.MEDIA_ROOT, 'track_tmp', '%d.wav' % (waveform.id))

    if not os.path.exists(track_tmp_file):
        download_original(waveform, track_tmp_file)
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
    os.unlink(track_tmp_file)
    os.unlink(track_tmp_wavfile)

@timed
def draw_peaks(waveform):
    track_tmp_wavfile = os.path.join(settings.MEDIA_ROOT, 'track_tmp', '%d.wav' % (waveform.id))
    waveform_img = WaveformImage(width, 511, palette='custom', bgcolor=None, color=rgb(waveform.color))
    waveform_img_filename = os.path.join(settings.TMP_DIR,  '%s_w.png' % str(waveform.id))
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
    urllib.urlretrieve(waveform.track.url, local_path)
    print 'Downloaded %s to %s' % (waveform.track.url, local_path)

@task()
def create_waveform(waveform):
    if not waveform.track.peaks:
        get_peaks(waveform)
    draw_peaks(waveform)