from confluence_tool.myquery import MyQuery as pq

"""
<ac:confluence
  xmlns:ac="http://www.atlassian.com/schema/confluence/4/ac/"
    xmlns:ri="http://www.atlassian.com/schema/confluence/4/ri/"
      xmlns="http://www.atlassian.com/schema/confluence/4/">
"""

# def test_namespaces():
#     namespaces={'a': 'http://localhost/a', 'c': 'http://localhost/c'}
#     d = pq('<mine xmlns:a="http://localhost/a" xmlns:c="http://localhost/c"><a:b><c:d>hello</c:d><x>world</x><c:d>foo</c:d></a:b></mine>', parser='xml', namespaces=namespaces)
#     print "c|d", d('c|d')
#     print "a|b", d('a|b')
#     assert False

def test_myquery():
    namespaces={'a': 'http://localhost/a', 'c': 'http://localhost/c'}
    d = pq('<a:b><c:d>hello</c:d><x>world</x><c:d>foo</c:d></a:b>',
        parser='xml', namespaces=namespaces)

    assert str(d('c|d')) == '<c:d>hello</c:d><c:d>foo</c:d>'
