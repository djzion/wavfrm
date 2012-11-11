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
        self.assertEqual(resp._headers['content-type'][1], 'image/png')
        pass

class EchonestTest(TestCase):
    url = 'http://unhearduv.com/wp-content/uploads/2012/06/1-Pericles-Rise-of-the-Jellyfish.mp3'
    tmp_filename = os.path.join('/tmp', 'echonest.png')
    pickled_at = os.path.join('/tmp', 'echonest_test_track_cache')

    def setUp(self):
        config.ECHO_NEST_API_KEY="QGSW4XPT3YCHCIE61"

        if True or not os.path.exists(self.pickled_at):
            self.track = track_from_url(self.url)
            pickle.dump(self.track, open(self.pickled_at, 'w'), pickle.HIGHEST_PROTOCOL)
        else:
            self.track = pickle.load(open(self.pickled_at, 'r'))

    def test_track_from_url(self):
        waveform = WaveformFactory.create_waveform(self.url, self.tmp_filename)
        from drawing import overlay_bars
        overlayed_filename = overlay_bars(waveform, self.track)
        print 'Image at %s' % overlayed_filename

class WaveformFactory(object):

    @classmethod
    def create_waveform(cls, url, local_filename, params=None):
        if os.path.exists(local_filename): return cls.create_waveform_from_existing_file(local_filename, url)
        print 'Local file %s not found, creating waveform for %s' % (local_filename, url)
        c = Client()
        resp = c.get('/waveform/', {'url': url, 'async': 0})
        out = open(local_filename, 'w')
        out.write(resp.content)
        out.close()
        return models.Waveform.objects.order_by('-created')[0]

    @classmethod
    def create_waveform_from_existing_file(cls, local_filename, url):
        img_file = File(open(local_filename, 'r'))
        track = models.Track.objects.create(url = url, waveform_img = img_file)
        waveform = models.Waveform(
            track = track,
            waveform_img = img_file
        )
        waveform.save()
        return waveform