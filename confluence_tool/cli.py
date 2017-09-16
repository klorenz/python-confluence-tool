"""
Confluence Commandline Interface

test

x

y

"""

import pyaml, yaml, sys, json, logging
import argparse
from os.path import expanduser
from confluence import ConfluenceError, ConfluenceAPI
from textwrap import dedent

def have_data_on_stdin():
    import sys
    import select

    if select.select([sys.stdin,],[],[],0.0)[0]:
        print "Have data!"
    else:
        print "No data"

from pprint import pprint

logging.basicConfig()

OUTPUT_FORMAT = 'yaml'

# global arguments
argparser = argparse.ArgumentParser(
    epilog=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    )
argparser.add_argument('--json', action='store_true')
argparser.add_argument('-c', '--config', help="Configuration name", default=None)
argparser.add_argument('-C', '--config-file', help="Configuration file (defaults to ~/.confluence-py.yaml)", default=None)
argparser.add_argument('-b', '--baseurl', help="Confluence Base URL e.g. http://example.com/confluence", default=None)
argparser.add_argument('-u', '--username', help="Username for logging in (if not present, tried to read from netrc)", default=None)
argparser.add_argument('-p', '--password', help="Password for logging in (if not present, tried to read from netrc)", default=None)
argparser.add_argument('-d', '--debug', action="store_true", help="Get more information on exceptions", default=None)

commands = argparser.add_subparsers()

class Config:
    def __init__(self, **args):
        self.args = args

    def __getattr__(self, name):
        if name == 'config':
            self.config = self.readConfig()
            return self.config

        if name == 'config_file':
            if self.args['config_file']:
                self.config_file = self.args['config_file']
            else:
                self.config_file = expanduser('~/.confluence-py.yaml')

            return self.config_file

        if name == 'confluence_api':
            self.confluence_api = self.getConfluenceAPI()
            return self.confluence_api

        try:
            return self[name]
        except KeyError:
            pass

        raise AttributeError(name)

    def __getitem__(self, name):
        return self.args[name]

    def readConfig(self):
        with open(self.config_file, 'r') as f:
            return yaml.load(f)

    def writeConfig(self):
        with open(self.config_file, 'w') as f:
            pyaml.p(self.config, file=f)

    def getConfig(self):
        result = {}

        result.update(
            baseurl  = self.args.get('baseurl'),
            username = self.args.get('username'),
            password = self.args.get('password'),
            )

        if not result['baseurl'] or self.args.get('config'):
            config_name = self.args.get('config', 'default') or 'default'
            result.update(**self.config[config_name])

        return result

    def setConfig(self):
        config_name = self.args.get('config', 'default')
        self.config[config_name] = dict(
            baseurl  = self.args.get('baseurl'),
            username = self.args.get('username'),
            password = self.args.get('password'),
        )
        self.writeConfig()

    def getConfluenceAPI(self):
        return ConfluenceAPI(self.getConfig())


class arg:
    def __init__(self, *args, **opts):
        self.args = args
        self.opts = opts
    def apply(self, parser):
        parser.add_argument(*self.args, **self.opts)

def command(name, *args, **opts):
    def factory(func):
        _doc = dedent(func.__doc__)
        try:
            help, desc = _doc.split("\n\n", 1)

        except:
            help = _doc
            desc = ''

        command = commands.add_parser(name, help=help, epilog=desc, formatter_class=argparse.RawDescriptionHelpFormatter)
        for a in args:
            if isinstance(a, arg):
                a.apply(command)
            else:
                command.add_argument(a)

        command.set_defaults(action=func)

        return func

    return factory


def dump(obj):
    if OUTPUT_FORMAT == 'yaml':
        try:
            pyaml.p(obj)
            return
        except ImportError:
            pass

    json.dump(obj, sys.stdout, indent=2)

@command('page-prop-get',
    arg('cql', help="SPACE:title, pageID or CQL"),
    arg('-f', '--filter', help="page property filter in format pageprop==value or pageprop!=value", default=None),
    arg('props', nargs="*", help="properties to retrieve"),
    )
def cmd_page_prop_get(config):
    """\
    Get page properties.

    For each page there is printed a YAML document with `id`, `title` and
    `spacekey`.  Page properties are printed under `pageProperties`.

    Optionally you can pass some page property filter expressions to filter
    pages on page properties additionally to CQL query.
    """
    confluence = config.getConfluenceAPI()
    first = True

    for pp in confluence.getPagesWithProperties(config.cql, config.filter):
        if not first:
            print("---")
        else:
            first = False

        result = pp.dict("id", "spacekey", "title")
        result['pageProperties'] = dict(pp.getPageProperties(*config.props))

        pyaml.p(result)


@command('page-prop-set',
    arg('cql', nargs="?", help="SPACE:title, pageID or CQL"),
    arg('-f', '--filter', help="page property filter in format pageprop==value or pageprop!=value", default=None),
    arg('propset', nargs="*", help="property setting expression"),
    arg('file', nargs="*", help="file to read data from")
    )
def cmd_page_prop_set(config):
    """\
    Set page properties.

    # Details

    There are multiple ways of setting page properties.  CQL and page property
    filters are working like in `page-prop-get` command and select pages to
    edit properties.

    # Setting page properties via arguments

    You can add multiple `propset` epressions.  A Propset expression is:

    * `propname:=value` -
      Replace current property with this value.  Value may be JSON or a string.

    * `propname+=value` -
      add value to current property value.

    * `propname-=value` -
      remove value from current property value.

    * `propname--` -
      remove property

    This way default templates for rendering properties are used.


    # Setting page properties via YAML from STDIN

    A document may have following values:

    - `page` - specify a page to be changed
    - `templates` - dictionary of templates with following names:
      - `user` - to render user names.  Gets userkey
      - `page` - to render page Gets spacekey, title
      - `link` - to render link Gets href, caption
      - `list` - to render a list
      - `PROPKEY-TYPE`, where PROPKEY is valid propkey and TYPE is one of the
        above.  This will be used as templates only for that key
    - `pages` - list of documents like this
    - `pagePropertiesEditor` - Define how to change page properties


    """

    pprint(config.args)

    sys.exit(0)

    config.args.file

    confluence = config.getConfluenceAPI()
    first = True

    PROPSET = re.compile(r'^(.*?)([:+-])=(.*)$')
    opmap = {
        ':': 'replace',
        '+': 'add',
        '-': 'remove',
    }

    files = []

    # handle propset
    propset = {}
    for prop in config.args.propset:
        if prop.endswith('--'):
            propset[prop[:-2]] = 'delete'
        else:
            m = PROPSET.match(prop)
            if m:
                (name, op, value) = m.groups()
                if name not in propset:
                    propset[name] = {}

                _prop = propset[name]
                op = opmap[op]
                if op not in _prop:
                    _prop[op] = value
                else:
                    if not isinstance(_prop[op], list):
                        _prop[op] = [ _prop[op] ]
                    _prop[op].append(vlaue)

            else:
                files.append(prop)

    # handle filenames
    input = ''
    for filename in files:
        if input != '':
            input += "---\n"
        if filename == '-':
            input += sys.stdin.read()
        else:
            with open(filename, 'r') as f:
                input += f.read()

    documents = []
    # parse yaml multidocument
    if input:
        documents = documents + yaml.safe_load_all(input)

    if len(propset):
        document = {
            'page': config.args.cql,
            'pagePropertiesEditor': propset,
        }
        documents = [document] + documents
    else:
        if config.args.cql:
            if len(documents) == 1:
                documents = [ {
                    'page': config.args.cql,
                    'pagePropertiesEditor': documents[0]
                } ]

    for doc in documents:
        for page in confluence.setPageProperties(doc):
            print "updated {}".format(page['id'], )


def main(argv):
    args = argparser.parse_args(argv)
    opts = vars(args).copy()
    del opts['action']

    global OUTPUT_FORMAT
    if 'json' in opts:
        if opts['json']:
            OUTPUT_FORMAT = 'json'
        del opts['json']

    config = Config(**opts)
    try:
        args.action(config)
    except ConfluenceError as e:
        dump(json.loads(str(e)))
    except Exception as e:
        if config.debug:
            import traceback
            traceback.print_exc()
        else:
            sys.stderr.write("%s\n" % e)

        return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]) or 0)
