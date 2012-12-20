import re

import urllib, urlparse

from bs4 import BeautifulSoup

from django.core.cache import cache

from imagedimensions.tasks import fetch_dimensions

RE_IMG = re.compile('<img.*?/>')


class ImageDimensionsMiddleware(object):

    def process_response(self, request, response):        
        if 'text/html' in response['Content-Type']:
            path = request.build_absolute_uri()
            def replace_img(match):
                img_str = match.group(0)
                img = BeautifulSoup(img_str).img
                
                if 'width' in img.attrs or 'height' in img.attrs:
                    return img_str
                url = urlparse.urljoin(path, img['src'])
                dim  = cache.get('imagedimensions-%s'%urllib.quote(url))
                if dim is None:
                   fetch_dimensions.delay(url)
                   return img_str
                w, h = dim
                if w and h:
                    img['width'] = w
                    img['height'] = h
                return str(img)
            
                            
            response.content = re.sub(RE_IMG, replace_img, response.content)
        return response
