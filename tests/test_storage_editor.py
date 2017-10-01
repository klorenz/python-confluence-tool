from textwrap import dedent
from confluence_tool.storage_editor import StorageEditor

def test_storage_editor_replace_content():
    e = StorageEditor(actions=dedent("""
        select: p
        content: foo
    """))
    assert e.edit("<p></p>") == "<p>foo</p>"

def test_storage_editor_append_content():
    e = StorageEditor(actions=dedent("""
        select: ul
        action: append
        content: "<li>second</li>"
    """))
    assert e.edit("<ul><li>first</li></ul>") == "<ul><li>first</li><li>second</li></ul>"

def test_storage_editor_replace_content_from_template():
    e = StorageEditor(
        actions = dedent("""
            select: div
            action: append
            content: <ul>{{#list}}<li>{{value}}</li>{{/list}}</ul>
            data:
                list:
                    - value: first
                    - value: second
        """)
    )
    assert e.edit("<div></div>") == "<div><ul><li>first</li><li>second</li></ul></div>"

def test_storage_editor_remove_item():
    e = StorageEditor(
            actions = dedent("""
                - select: p:last-child
                  action: remove
            """)
        )
    assert e.edit("<p>first</p><p>second</p>") == "<p>first</p>"
