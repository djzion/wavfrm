import os, logging
from PIL import Image, ImageFont, ImageDraw
from django.conf import settings

HEX = '0123456789abcdef'

def rgb(triplet):
    triplet = triplet.lower()
    return (HEX.index(triplet[0])*16 + HEX.index(triplet[1]),
            HEX.index(triplet[2])*16 + HEX.index(triplet[3]),
            HEX.index(triplet[4])*16 + HEX.index(triplet[5]))

def triplet(rgb):
    return hex(rgb[0])[2:] + hex(rgb[1])[2:] + hex(rgb[2])[2:]

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
        bar_alpha = 200 - int(bar['confidence'] * 127)
        if bar_alpha > 255: bar_alpha = 255
        draw.line((dx, 0, dx, img.size[1]), fill=(200, 0, 0, bar_alpha), width=bar_width)

    for beat in echo_track.bars:
        dx = int(beat['start'] * pixels_per_second)
        draw.line((dx, 0, dx, img.size[1]))

    out_path = os.path.join(os.path.split(waveform.waveform_img.path)[0], 'overlayed.png')
    fp_out = open(out_path, 'w')
    img.save(fp_out)
    return fp_out.name