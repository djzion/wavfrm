import os, logging
from PIL import Image, ImageFont, ImageDraw
from django.conf import settings

def overlay_bars(waveform, echo_track):
    img = Image.open(waveform.waveform_img.path)
    draw = ImageDraw.Draw(img)
    pixels_per_second = float(img.size[0]) / int(echo_track.meta['seconds'])
    sections = reversed(echo_track.sections)
    bar_section = None

    for bar in echo_track.sections:
        """
        try:
            _bar_section = next(section for section in echo_track.sections if section['start'] <= bar['start'])
            if bar_section is not None and _bar_section['start'] > bar_section['start']:
                logging.info('Bar %s starts a new section %s' % (bar, _bar_section))
                new_section = True
            else:
                new_section = False
                bar_section = _bar_section
        except StopIteration:
            pass
        """
        dx = int(bar['start'] * pixels_per_second)
        bar_width = int(bar['confidence']) * 3
        #if new_section: bar_width += 2
        bar_alpha = 128 - int(bar['confidence'] * 127)
        draw.line((dx, 0, dx, img.size[1]), fill=(0, 0, 0, bar_alpha), width=bar_width)

    #for beat in echo_track.beats:
    #    dx = int(beat['start'] * pixels_per_second)
    #    draw.line((dx, 0, dx, img.size[1]))

    out_path = os.path.join(os.path.split(waveform.waveform_img.path)[0], 'overlayed.png')
    fp_out = open(out_path, 'w')
    img.save(fp_out)