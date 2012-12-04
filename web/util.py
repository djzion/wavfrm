import os

def humanize_filename(filename):
    filename = os.path.splitext(filename)[0]
    replace_map = {
        '-': ' ',
        '_': ' ',
        '.': ' '
    }
    for search, replace in replace_map.iteritems():
        filename = filename.replace(search, replace)
    return filename