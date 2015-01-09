# -*- coding: utf-8 -*-

import sys
import os

#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.viewcode',
    'sphinx.ext.viewcode',
    'sphinxarg.ext'
]

# Document constructors (off by default)
autoclass_content = 'both'

templates_path = ['_templates']

source_suffix = '.rst'

master_doc = 'index'

project = u'robot_upstart'
copyright = u'2015, Mike Purvis'

# Get version number from package.xml.
import xml.etree.ElementTree as etree
tree = etree.parse('../package.xml')
version = tree.find("version").text
release = version

pygments_style = 'sphinx'

html_theme = 'nature'

htmlhelp_basename = 'robot_upstartdoc'
