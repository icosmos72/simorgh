"""
This module contains:
  - A schemas object representing parsed JSON-schemas from the schemas directory
  - A SchemaBasedRESTEndpoint class definition, for defining REST endpoints based on JSON-Schema
  - A rest-endpoints object which is suitable for use with cherrypy as a server object
"""
__author__ = 'Matthew Wampler-Doty'

import os.path
import pkg_resources
import json
import cherrypy
import collections
from database import db

# Parse all of the schema data from the schemas subdirectory and make a dictionary
schema_dir = 'schemas'
schemas = {
    os.path.splitext(schema)[0]:
        json.loads(pkg_resources.resource_string(__name__, os.path.join(schema_dir, schema)))
    for schema in pkg_resources.resource_listdir(__name__, schema_dir)
    }


class SchemaBasedRESTEndpoint(object):
    exposed = True

    def __init__(self, schema):
        # TODO: make a schema for validating schema
        assert 'id' in schema['properties'], "Schema does not specify an 'id' property:\n\n{}".format(
            json.dumps(schema, sort_keys=True, indent=4, separators=(',', ': ')))
        assert len(schema['properties']['type']['enum']) is 1, \
            "Schema must specify a unique 'type' property:\n\n{}".format(
                json.dumps(schema, sort_keys=True, indent=4, separators=(',', ': ')))
        self.schema = schema
        self.name = schema['properties']['type']['enum'][0]

    __init__.exposed = False

    def process_data(self, data):
        """Process data from a POST or PUT call"""
        import jsonschema
        jsonschema.validate(data, self.schema)
        return db.insert(data)

    process_data.exposed = False

    @cherrypy.tools.json_out()
    def GET(self):
        from tinydb import where
        return db.search(where('type') == self.name)

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def POST(self):
        return self.process_data(cherrypy.request.json)

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def PUT(self):
        return self.process_data(cherrypy.request.json)


# Create a rest_endpoints object suitable for CherryPy
rest_endpoints = (collections.namedtuple('DataRESTEndpoints', ['exposed', 'favicon_ico', 'conf'] + schemas.keys()))(
    exposed=True,
    # This needs to be set apparently...
    favicon_ico=None,
    conf={
        os.path.join('/', schema_name): {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'application/json')],
        } for schema_name in schemas},
    **{schema_name: SchemaBasedRESTEndpoint(schema) for schema_name, schema in schemas.iteritems()})
