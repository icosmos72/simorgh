__author__ = 'Matthew Wampler-Doty'
import cherrypy


def server(path='/data', port=8080, serve=True):
    """Run the server using CherryPy"""
    import data
    assert isinstance(path, str), "Path must be a string"

    cherrypy.tree.mount(data.rest_endpoints, path, data.rest_endpoints.conf)

    if serve is True:
        cherrypy.config.update({'server.socket_port': port})
        cherrypy.engine.start()
        cherrypy.engine.block()
