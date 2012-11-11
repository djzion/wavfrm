import os
from django.db import models
from django.conf import settings
from django.contrib.admin.models import User
from picklefield.fields import PickledObjectField

def get_task_path(instance, filename, media_subfolder):
    return media_subfolder + '/' + filename

def choices(choice_cls):
    return [(attr, attr) for attr in choice_cls.__dict__.keys() if not attr.startswith('_')]

class MockFileField(object):
    """
    Created to workaround the Django behavior FileField behavior, with similar API
    1) Not allowing files that already exist (we want to avoid moving them)
    2) Saving files with an "_n" on name conflicts (we want to use prexisting files)
    3) Not deleting file when the model is deleted   
    """
    path = None
        
    def __init__(self, path, media_subfolder):
        self.path = path
        self.media_subfolder = media_subfolder

    def get_url(self):
        return settings.MEDIA_URL + get_task_path(None, os.path.basename(self.path), self.media_subfolder)
    url = property(get_url)
 
    def open(self):
        return open(self.path)
    
    def delete(self):
        os.remove(self.path)

    def __str__(self):
        return self.path

    def __repr__(self):
        return self.path
    
class Track(models.Model):
    url = models.CharField(max_length=255)
    title = models.CharField(max_length=255, null=True)
    duration = models.FloatField(null=True)
    waveform_img = models.ImageField(upload_to='waveforms', null=True)
    peaks = models.TextField(null=True)
    centroids = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    echonest_analysis = models.TextField(null=True)
    user = models.ForeignKey(User, null=True)
    
    def get_waveform(self):
        return MockFileField(self.waveform_img_path, 'waveforms')
    waveform = property(get_waveform)
    
    def get_spectrum(self):
        return MockFileField(self.spectrum_img_path, 'waveforms')
    waveform = property(get_waveform)

class WaveformStatus:
    waiting = 'waiting'
    downloading = 'downloading'
    processing = 'processing'
    drawing = 'drawing'
    echonest = 'echonest'
    complete = 'complete'
    error = 'error'

class Waveform(models.Model):
    _status_choices = WaveformStatus
    track = models.ForeignKey(Track)
    color = models.CharField(max_length=6, default='006699')
    color_centroid = models.CharField(max_length=6, null=True)
    bgcolor = models.CharField(max_length=20, null=True)
    waveform_img = models.ImageField(upload_to='waveforms', null=True)
    spectrum_img = models.ImageField(upload_to='waveforms', null=True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=choices(WaveformStatus), default='waiting', max_length=50)

    def __str__(self):
        return '%s %s' % (self.waveform_img, self.status)

    def to_dict(self):
        data = self.__dict__
        del data['created']
        return data
    