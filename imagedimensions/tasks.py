import urllib
import ImageFile

from django.core.cache import cache

from celery.decorators import task


def get_image_size(uri):
    file = urllib.urlopen(uri)
    p = ImageFile.Parser()
    data = file.read()#file.read(1024)
    if not data:
        return None
    p.feed(data)
    if p.image:
        return p.image.size
    file.close()
    #not an image
    return None

@task
def fetch_dimensions(url):
    dim = get_image_size(url)
    key = urllib.quote('imagedimensions-%s'%url)
    if dim:
        cache.set(key, dim)
    else:
        cache.set(key, (0,0))
