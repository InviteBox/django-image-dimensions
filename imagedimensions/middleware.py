from imagedimensions import add_dimensions

class ImageDimensionsMiddleware(object):

    def process_response(self, request, response):        
        if 'text/html' in response['Content-Type']:
            path = request.build_absolute_uri()
            response.content, dimensions_found = add_dimensions(response.content, path)
        return response
