from .cli import *
import sys

@command('show',
    positional_arg_cql,
    arg_filter,
    arg_expand,
    arg_write_format,
    arg_format,
    mutually_exclusive(
        arg('--storage', action="store_true", help="convenience for: -e 'body.storage' -F '{body[storage][value]}'"),
        arg('--html', action="store_true", help="convenience for: -e 'body.view' -F '{body[view][value]}'"),
        arg('--ls', action="store_true", help="convenience for: -F '{id} {spacekey} {title}'"),
    ),
#    arg('-d', '--data', help="filename containing data selector in YAML or JSON format"),
    arg('field', nargs="*", help='field to dump')
)
def show(config):
    """show a confluence item


    """


    """show a confluence item

    If specifying data selector file, there is added a special field
    body['data'] to each page.

    Format of selector file:

    select: <CSS Selector for jQuery>
    list:
        - attr: href
          name: href

    Following keys:

    - list: each item produces a list item.  Input is current selected element.
    - object: each item produces a object property.  Each item must have "name"
        key for specifing the properties name
    - attr: read named attribute from current selected element
    - select: find elements using this selector.  For each of them apply current
      spec
    - text: 'text' or 'html'.  this is the default and default is to return
        'text'.


    """
    first = True

    mustache, format, printf = None,None,None

    output_filter = lambda x: x

    if not config.get('format') and not config.get('expand'):
        if config.get('html'):
            config['format'] = u'{body[view][value]}'
            config['expand'] = 'body.view'

            from html5print import HTMLBeautifier
            output_filter = lambda x: HTMLBeautifier.beautify(x, 4)

        elif config.get('storage'):
            config['format'] = u'{body[storage][value]}'
            config['expand'] = 'body.storage'

            from html5print import HTMLBeautifier
            output_filter = lambda x: HTMLBeautifier.beautify(x, 4)

        elif config.get('ls'):
            config['format'] = u'{id}  {spacekey}  {title}'
            config['field'] = ['id', 'spacekey', 'title']

    results = []
    kwargs = config.dict('cql', 'expand', 'filter')
    kwargs['cql'] = config.confluence_api.resolveCQL(kwargs['cql'])

    for page in config.confluence_api.getPages(**kwargs):
        results.append(page.dict(*config['field']))

    if config.get('format'):
        for result in results:
            if '{}' in config['format']:
                fields = [ result[f] for f in config['field'] ]
                print config['format'].format(*fields)

            print output_filter(unicode(config['format']).format(**result))

    elif config.get('data'):
        if config.get('data') == '-':
            data = get_list_data(sys.stdin.read())
        else:
            with open(config.get('data'), 'r') as f:
                data = get_list_data(f.read())

        from ..data_generator import generate_data

        pyaml.p(generate_data(data, results))

    else:
        if len(results) == 1:
            results = results[0]

        if config['write'] == 'json':
            import json
            json.dump(results, sys.stdout)

        elif config['write'] == 'yaml':
            import pyaml
            pyaml.p(results)