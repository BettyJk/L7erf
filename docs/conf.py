# conf.py for L7erf Bot Documentation

# -- Project information -----------------------------------------------------

project = 'L7erf Bot'
author = 'Jouak Bouthayna et Hajar el Hadri'
release = '15/12/2024'
copyright = 'Copyright 2024, Jouak Bouthayna et Hajar el Hadri'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    'sphinx.ext.autodoc',   # Automatic documentation generation from docstrings
    'sphinx.ext.viewcode',  # Add links to source code
    'sphinx.ext.napoleon',  # Support for Google-style docstrings
    'sphinx_rtd_theme',     # For Read the Docs theme
]

# The master toctree document.
master_doc = 'index'

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.
html_theme = 'sphinx_rtd_theme'

# -- Options for LaTeX output -------------------------------------------------

# For a simple document, this is probably unnecessary.
latex_documents = [
    ('index', 'L7erfBot.tex', 'L7erf Bot Documentation',
     'Jouak Bouthayna et Hajar el Hadri', 'manual'),
]

# -- Options for manual page output ----------------------------------------

man_pages = [
    ('index', 'L7erfBot', 'L7erf Bot Documentation',
     ['Jouak Bouthayna et Hajar el Hadri'], 1)
]

# -- Options for Texinfo output ---------------------------------------------

texinfo_documents = [
    ('index', 'L7erfBot', 'L7erf Bot Documentation',
     'Jouak Bouthayna et Hajar el Hadri', 'L7erfBot', 'One line description of project.',
     'Miscellaneous'),
]

# -- Extension configuration -------------------------------------------------

# For example, to enable the Napoleon extension for Google-style docstrings:
napoleon_google_docstring = True
