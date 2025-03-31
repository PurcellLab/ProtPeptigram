# Configuration file for the Sphinx documentation builder.
import os
import sys
from datetime import datetime

# Add the project root directory to the path so Sphinx can find the modules
sys.path.insert(0, os.path.abspath('..'))

# Project information
project = 'ProtPeptigram'
copyright = f'{datetime.now().year}, Sanjay SG Krishna'
author = 'Sanjay SG Krishna'

# The version info for the project
version = '0.1'
release = '0.1.0'

# General configuration
extensions = [
    'sphinx.ext.autodoc',     # Include documentation from docstrings
    'sphinx.ext.napoleon',    # Support for NumPy and Google style docstrings
    'sphinx.ext.viewcode',    # Add links to the source code
    'sphinx.ext.intersphinx', # Link to other project's documentation
    'sphinx_autodoc_typehints',  # Use type hints for documentation
    'myst_parser',            # Parse Markdown files
    'nbsphinx',               # Include Jupyter notebooks
]

# Add any paths that contain templates here
templates_path = ['_templates']

# List of patterns to exclude from source files
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '**/__pycache__']

# The theme to use for HTML and HTML Help pages
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'navigation_depth': 4,
    'titles_only': False,
}

# Add any paths that contain custom static files (such as style sheets)
html_static_path = ['_static']

# Configure autodoc to include both class and __init__ docstrings
autoclass_content = 'both'

# Sort members by type in autodoc
autodoc_member_order = 'groupwise'

# Document Python Code
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
}

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'pandas': ('https://pandas.pydata.org/pandas-docs/stable/', None),
}