django-image-dimensions
=======================

Automatically add dimension attributes to all &lt;img&gt; tags in a response to improve rendering speed on the client.

##Rationale

Specifying image dimensions in HTML improves both percieved and actual client-side rendering performance by preventing reflow. However, maintaining explicit dimensions in templates is tedious and impractical in some cases. This middleware solves that in a plug-and-play manner by automatically setting dimensions in all &amp;img&amp; tags in a response.

##Requirements

* `django-celery` to run image fetch and dimensions calculations in the background
* `PIL`
* A cache that is shared between web server and celery (e.g. memcached)

##Installation
1. Run `pip install django-image-dimensions`
2. Add `'imagedimensions'` app to `INSTALLED_APPS` 
3. Add `'imagedimensions.middleware.ImageDimensionsMiddleware'` to `MIDDLEWARE_CLASSES`




 