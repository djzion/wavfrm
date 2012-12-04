import os

def humanize_filename(filename):
    filename = os.path.splitext(filename)[0]
    replace_map = {
        '-': ' ',
        '_': ' ',
        '.': ' '
    }
    [filename.replace(search, replace) for search, replace in replace_map.iteritems()]
    return filename