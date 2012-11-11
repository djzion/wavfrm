from celery.decorators import task
from services import get_peaks, get_echonest_data_for_track, draw_peaks
from models import WaveformStatus

@task
def create_waveform_task(waveform, force_regen):
    if force_regen or not waveform.track.peaks:
        waveform.status = WaveformStatus.processing
        waveform.save()
        get_peaks(waveform, force_regen)

    draw_peaks(waveform)

    if not waveform.track.echonest_analysis:
        waveform.status = WaveformStatus.echonest
        waveform.save()
        get_echonest_data_for_track(waveform.track)

    waveform.status = WaveformStatus.complete
    waveform.save()

    return waveform