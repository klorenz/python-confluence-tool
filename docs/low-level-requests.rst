Low Level Requests
==================

You can do low-level requests to the API with subcommands ``get``, ``post``,
``put`` and ``delete``.

In this documentation the examples from `Confluence REST API Examples`_ page
are written with the use of ``ct`` low level requests and also in convenience
commands, if available.

.. _Confluence REST API Examples:
   https://developer.atlassian.com/server/confluence/confluence-rest-api-examples/


Configuration (with password ``admin``) would be done with::

    ct -b http://localhost:8080/confluence -u admin config


GET Requests
------------

Finding blog posts::

    ct get /rest/api/content type=blogpost start=0 limit=10 expand=space,history,body.view,metadata.labels


Browse Content::

    ct get /rest/api/content/3965072 expand=body.storage
    ct show 3965072 -e body.storage


Find a page by title and space key::

    ct get /rest/api/content title=myPage%20Title spaceKey=TST expand=history
    ct show "TST:myPage Title" -e history


POST Requests
-------------

Create a new page::

  ct post /rest/api/content/ <<!
  type: page
  title: new page
  space:
    key: TST
  body:
    storage:
      value: |
        <p>This is <br/>
        a new page</p>
      representation: storage
  !

