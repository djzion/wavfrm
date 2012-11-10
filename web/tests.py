import os, pickle
from django.test import TestCase, Client
from django.conf import settings
from django.core.files import File
from pyechonest.track import *
from pyechonest import config
import models

class ApiTest(TestCase):
    def setUp(self):
        pass

    def test_basic(self):
        c = Client()
        resp = c.get('/waveform/', {'url': 'http://localhost:8000/static/audio/perspective.mp3', 'async': 0})
        pass

class EchonestTest(TestCase):
    url = 'http://unhearduv.com/wp-content/uploads/2012/06/1-Pericles-Rise-of-the-Jellyfish.mp3'
    pickled_at = '_track_picked'

    def setUp(self):
        config.ECHO_NEST_API_KEY="QGSW4XPT3YCHCIE61"

        if not os.path.exists(self.pickled_at):
            self.track = track_from_url(self.url)
            pickle.dump(self.track, open(self.pickled_at, 'w'), pickle.HIGHEST_PROTOCOL)
        else:
            self.track = pickle.load(open(self.pickled_at, 'r'))

    def test_track_from_url(self):
        img_file = File(open(os.path.join(settings.MEDIA_ROOT, 'waveforms', '1_w_136.png'), 'r'))
        track = models.Track.objects.create(url = self.url, waveform_img = img_file)
        waveform = models.Waveform(
            track = track,
            waveform_img = img_file
        )
        waveform.save()
        from tasks import create_waveform
        #create_waveform(waveform)

        from drawing import overlay_bars
        overlay_bars(waveform, self.track)
        print track