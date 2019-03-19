Querying confluence
===================

You can pass `CQL`_ queries to many commands, which you can use to do
`advanced searching in confluence`_.  Due to the fact that for most commands
in the `Confluence Server REST API`_ require a Page ID and finding out Page IDs
is always a cumbersome extra step, there is a convenience extra syntax for
in Confluence Tool, which you can use also, if CQL is required.

.. _CQL: https://developer.atlassian.com/confdev/confluence-server-rest-api/advanced-searching-using-cql
.. _advanced searching in confluence: https://developer.atlassian.com/server/confluence/advanced-searching-using-cql/
.. _Confluence Server REST API: https://developer.atlassian.com/server/confluence/confluence-server-rest-api/

Confluence Tool Convenience Syntax
----------------------------------

Let us start with an example::

   ct show DOC: --ls

will list all pages in a space with key "DOC", which is equivalent to using the
CQL query::

   ct show 'space = DOC' --ls


Here is a mapping, how Confluence Tool Convenience Syntax translates to CQL:

====================================  ==========================================
Confluence Tool Convenience Syntax    CQL
====================================  ==========================================
DOC:Example Page                      space = DOC AND title = "Example Page"
DOC:                                  space = DOC
:Example Page                         title = "Example Page"
12345                                 ID = 12345
api/content/12345                     ID = 12345
DOC:Example Page>                     parent = <ID of result>
DOC:Example Page>>                    ancestor = <ID of result>
====================================  ==========================================


Specifying a page
-----------------

A page can be specified using the space key and the page's title.
``DOC:Example`` specifies a page titled "Example" in space with key "DOC".

So a query with the form::

  <SPACEKEY> ":" <TITLE>

Translates to CQL::

  space = <SPACEKEY> and title = "<TITLE>"

You can also use the numeric ID for specifying a page or the URI of a page as
it is returned from REST API requests::

====================================  ===============
12345                                 ID = 12345
api/content/12345                     ID = 12345
====================================  ===============


Querying children of a page
---------------------------

For querying the childrens of a page, you can use the ">" suffix::

  :Example>

Will do a query for ``:Example``.  Let there be two pages in your Confluence
instance having the title "Example", with pageids 12345 and 23456.  Then
this will resolve to the CQL query::

  (parent = 12345 OR parent = 23456)


Querying descendants of a page
------------------------------

This works exactly like the children query.  Having an example like in
`Querying children of a page`_  using the ">>" suffix::

  :Example>>

Will finally do the CQL query::

  (ancestor = 12345 OR ancenstore = 23456)
