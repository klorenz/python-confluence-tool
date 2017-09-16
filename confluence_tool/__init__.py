"""
This module provides the main API of Confluence.  You can either import confluence_cli for having a confluence CLI or you import the API.
"""

from .confluence_api import ConfluenceError, ConfluenceAPI
from .cli import main as confluence_cli
