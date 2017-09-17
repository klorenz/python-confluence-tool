from confluence_tool.myquery import MyQuery as pq

def test_myquery():
    namespaces={'a': 'http://localhost/a', 'c': 'http://localhost/c'}
    d = pq('<a:b><c:d>hello</c:d><x>world</x><c:d>foo</c:d></a:b>',
        parser='xml', namespaces=namespaces)

    assert str(d('c|d')) == '<c:d>hello</c:d><c:d>foo</c:d>'
