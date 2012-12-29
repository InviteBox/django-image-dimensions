from django.template import Library, Node, TemplateSyntaxError, Variable, VariableDoesNotExist
from django.template import resolve_variable
from django.core.cache import cache
from django.utils.encoding import force_unicode
from django.utils.http import urlquote
from django.utils.hashcompat import md5_constructor

from imagedimensions import add_dimensions

register = Library()

class CacheNode(Node):
    def __init__(self, nodelist, expire_time_var, fragment_name, vary_on):
        self.nodelist = nodelist
        self.expire_time_var = Variable(expire_time_var)
        self.fragment_name = fragment_name
        self.vary_on = vary_on

    def render(self, context):
        try:
            expire_time = self.expire_time_var.resolve(context)
        except VariableDoesNotExist:
            raise TemplateSyntaxError('"cache" tag got an unknown variable: %r' % self.expire_time_var.var)
        try:
            expire_time = int(expire_time)
        except (ValueError, TypeError):
            raise TemplateSyntaxError('"cache" tag got a non-integer timeout value: %r' % expire_time)
        # Build a unicode key for this fragment and all vary-on's.
        args = md5_constructor(u':'.join([urlquote(resolve_variable(var, context)) for var in self.vary_on]))
        cache_key = 'template.cache.%s.%s' % (self.fragment_name, args.hexdigest())
        value = cache.get(cache_key)
        if value is None:
            print 'MISS'
            value = self.nodelist.render(context)
            value, dimensions_found = add_dimensions(value, context['request'].build_absolute_uri())
            print dimensions_found
            if dimensions_found:
                cache.set(cache_key, value, expire_time)
        return value

def do_cache(parser, token):
    nodelist = parser.parse(('endcache',))
    parser.delete_first_token()
    tokens = token.contents.split()
    if len(tokens) < 3:
        raise TemplateSyntaxError(u"'%r' tag requires at least 2 arguments." % tokens[0])
    return CacheNode(nodelist, tokens[1], tokens[2], tokens[3:])

register.tag('cache', do_cache)