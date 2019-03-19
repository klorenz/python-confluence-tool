Install
-------

Install confluence_tool using pip::

    pip install confluence_tool


Configuration
-------------

Configuration is done in a file named ``.confluence-tool.yaml`` in your home directory.  Passwords are
stored in your system's keystore.

There is one default configuration, but you can also have multiple configurations, either for accessing
one confluence instance with multiple users or to access multiple confluence instances.

For configuring the default, simply run::

    ct -b CONFLUENCE_URL -u USERNAME config

This will ask you for a password, which will then be stored in your system's
keystore.  If you want to change the password, you can run::

    ct -b CONFLUENCE_URL -u USERNAME config --update-password


If you want to setup another configuration, you can do so with specifying ``-c`` parameter::

    ct -c doc -b CONFLUENCE_URL -u USERNAME config

You then can specify ``-c doc`` as a global argument for any other command to use this configuration.
