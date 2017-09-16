import contextlib, re
#from pyquery import PyQuery
from pystache import Renderer
from os.path import dirname
#import pyquery.pyquery as pqmodule
from .myquery import MyQuery



# monkey patch PyQuery
# FIRST_TAG = re.compile(r'^<[^\s]+')
# _pyquery_fromstring = pqmodule.fromstring
# def fromstring(context, parser=None, custom_parser=None):
#     #print "parser", parser
#     #print "context 1", context
#     if parser == 'xml':
#         if context.startswith("<root>"):
#             context = ('<root class="xmlns-wrapper"'
#               +' xmlns:ac="http://www.atlassian.com/schema/confluence/4/ac"'
#               +' xmlns:ri="http://www.atlassian.com/schema/confluence/4/ri">'
#               +context[6:])
#             #print "context", context
#
#     return _pyquery_fromstring(context, parser=parser, custom_parser=custom_parser)
#
# pqmodule.fromstring = fromstring
#
# def _copy(self, *args, **kwargs):
#     kwargs.setdefault('namespaces', self.namespaces)
#     kwargs.setdefault('parser', self.parser)
#     return self.__class__(*args, **kwargs)
#
# PyQuery._copy = _copy
#
class StorageEditor:
    def __init__(self, confluence=None, templates=None, partials=None, actions=None):
        self.templates = templates
        self.partials = partials
        self.actions = actions
        self.confluence = confluence
        self.renderer = Renderer(
            search_dirs = "{}/templates".format(dirname(__file__)),
            file_extension = "mustache",
            )

    def edit(self, page):
        content = page['body']['storage']['value']
        Q = self.begin_edit(content)

        for action in self.actions:
            if 'data' in action:
                if 'template' in action:
                    content = self.renderer.render_name(action['template'], action['data'])
                else:
                    content = self.renderer.render(action['content'], action['data'])
            else:
                content = action['content']

            if 'type' in content:
                if content['type'] == 'wiki':
                    content = self.confluence.convertWikiToStorage(content)

            getattr(Q(action['select']), action.get('action', 'html'))(content)

        return self.end_edit()


    def begin_edit(self, content=None):
        if content is None:
            content = self.content

        self.pyquery = storage_query(content)

        return self.pyquery

    FIRST_OPENING_TAG = re.compile(r'^<root[^>]*>')
    LAST_CLOSING_TAG  = re.compile(r'</root>$')
    def end_edit(self, pyquery=None):
        if pyquery is None:
            pyquery = self.pyquery

        data = str(pyquery)
        return data

def edit(content):
    storage_editor = StorageEditor()
    pyquery = storage_editor.begin_edit(content)

    def end_edit(*args):
        return storage_editor.end_edit()

    pyquery.end_edit = end_edit
    return pyquery


def storage_query(content):
    namespaces = {
        'ac': 'http://www.atlassian.com/schema/confluence/4/ac',
        'ri': 'http://www.atlassian.com/schema/confluence/4/ri',
    }

    return MyQuery(content, parser='xml', namespaces=namespaces)