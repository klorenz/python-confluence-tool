# -*- coding: utf-8 -*-
import pytest, sys
from confluence_tool.page_properties import extract_data, get_page_properties, PagePropertiesEditor
from textwrap import dedent
from os.path import dirname
from pprint import pprint, pformat
import pyaml, yaml
from confluence_tool.storage_editor import storage_query

@pytest.fixture
def page_properties_html():
    with open(dirname(__file__)+"/fixtures/page_properties.html", 'r') as f:
        return f.read()

@pytest.fixture
def pp_page():
    with open(dirname(__file__)+"/fixtures/storage-data.yaml", 'r') as f:
        page = yaml.safe_load(f)
    page['body'] = {'storage': {}}

    with open(dirname(__file__)+"/fixtures/storage-data.html", 'r') as f:
         page['body']['storage']['value'] = f.read()

    return page

def test_get_page_properties(page_properties_html):
    pp = dict(get_page_properties(page_properties_html))
    assert set(pp.keys()) == set(['Name', 'Page refs', 'Person', 'Persons', 'External Link'])
    assert pp['Name'] == 'Test'
    assert pp['External Link'] == '[test link|http://google.com] [http://google.com]'
    assert pp['Page refs'] == ['[IT:Aachen Office]', '[IT:Bucharest Office]', '[IT:Simferopol Office]']
    assert pp['Person'] == '[~kiwi]'
    assert pp['Persons'] == ['[~kiwi]', '[~nini]']

def test_edit_page_properties_delete_prop(pp_page):
    pagePropertiesEditor = {
        'Username': 'delete'
    }

    assert '<th>Username</th>' in pp_page['body']['storage']['value']
    ppe = PagePropertiesEditor(pagePropertiesEditor)
    print "delete_prop"
    pprint(ppe.editor)
    body = ppe.edit(pp_page)
    assert '<th>Username</th>' not in body

def test_edit_page_properties_replace_prop(pp_page):
    edit_actions = {
        'Name': {'replace': "foo"}
    }
    body = PagePropertiesEditor(edit_actions).edit(pp_page)
    p = storage_query(body)
    assert p('th:contains(Name)').next().text() == 'foo'


def test_edit_page_properties_add_prop(pp_page):
    edit_actions = {
        'Name': {'add': "foo"}
    }
    body = PagePropertiesEditor(edit_actions).edit(pp_page)
    p = storage_query(body)

    assert p('th:contains(Name)').next().html() == dedent(u"""\
        <ul>
          <li>Kay-Uwe (Kiwi) Lorenz account</li>
          <li>foo</li>
        </ul>
    """)


def test_edit_page_properties_remove_prop(pp_page):
    edit_actions = {
        'Roles': {'remove': ['[IT:IT Observer role]', 'MasterCAM SDK Receiver role']}
    }
    #import rpdb2 ; rpdb2.start_embedded_debugger('foo')

    body = PagePropertiesEditor(edit_actions).edit(pp_page)
    p = storage_query(body)

    print p('th:contains(Roles)').next().html()

    assert p('th:contains(Roles)').next().html() == dedent(u"""\
        <ul>
          <li><ac:link>
          <ri:page ri:space-key="IT" ri:content-title="Team Leader role"/>
        </ac:link></li>
          <li><ac:link>
          <ri:page ri:space-key="IT" ri:content-title="Bitbucket role"/>
        </ac:link></li>
          <li><ac:link>
          <ri:page ri:space-key="IT" ri:content-title="Deploy Receiver role"/>
        </ac:link></li>
          <li><ac:link>
          <ri:page ri:space-key="IT" ri:content-title="CI Observer role"/>
        </ac:link></li>
          <li><ac:link>
          <ri:page ri:space-key="IT" ri:content-title="ARB Building Linking Release Member role"/>
        </ac:link></li>
        </ul>
    """)
