Filtering Query Results
=======================

Apart from the CQL you have in most commands two more options to filter query
results.  Depending on the option this will modify/extend the CQL query or will
filter the results from the CQL query.


Comala Workflow States
----------------------

Most commands provide ``--state`` option, which lets you filter on
Comala Workflow state of the page.  Providing the state argument will return
the last version of a page in the wanted state.

If you have a simple workflow having the states "Draft" and "Approved" and you
query ``--state Approved``, will return you the last approved version, even if
the current version is in Draft state.

The state parameter translates to an extension of the CQL query::

   (<Original CQL Query>) AND state = "Approved"


Filtering on Page Properties
----------------------------

If you work a lot with page properties, this is very helpful to filter the
results of a CQL by Page Properties.

======================  =========================================================
Filter Option           Description
======================  =========================================================
``-F <NAME>==<VALUE>``  Value of property ``<NAME>`` must be ``<VALUE>`` or if
                        value is a list, then ``<VALUE>`` must be one of the
                        list's elements.

``-F <NAME>!=<VALUE>``  Value of property ``<NAME>`` must not be ``<VALUE>`` or
                        if value is a list, then there must be no element
                        beeing ``<VALUE>``.

``-F '!<NAME>'``        There must be no property ``<NAME>`` in the page's
                        properties.

``-F '<NAME>?'``        There must exist a propert ``<NAME>`` in the page's
                        properties.
======================  =========================================================


