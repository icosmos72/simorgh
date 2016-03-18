import cherrypy
import time

class Temperatures(object):
    exposed = True

     @cherrypy.tools.accept(media='text/plain')
     def GET(self):
         return "foo"

     def POST(self,
              serial_number,
              channel,
              temperature,
              time_stamp=time.time() * 1000,
              manufacturer_name=None,
              product_name=None):
         return "bar"

     def PUT(self, another_string):
         cherrypy.session['mystring'] = another_string

