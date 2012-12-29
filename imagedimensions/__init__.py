import re

import urllib, urlparse

from bs4 import BeautifulSoup

from django.core.cache import cache

from imagedimensions.tasks import fetch_dimensions

RE_IMG = re.compile('<img.*?/>')


def add_dimensions(html, base_uri):    
    class replace_img:
        def __init__(self):
            self.dimensions_found = True
        def __call__(self, match):
            img_str = match.group(0)
            img = BeautifulSoup(img_str).img

            if 'width' in img.attrs or 'height' in img.attrs:
                return img_str
            url = urlparse.urljoin(base_uri, img['src'])
            dim  = cache.get('imagedimensions-%s'%urllib.quote(url))
            if dim is None:
               fetch_dimensions.delay(url)
               self.dimensions_found = False           
               return img_str
            w, h = dim
            if w and h:
                img['width'] = w
                img['height'] = h
            return str(img)
    replacer = replace_img()
    val = re.sub(RE_IMG, replacer, html)
    return val, replacer.dimensions_found
