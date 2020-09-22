# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import json

sys.path.insert(0, os.path.abspath("../../"))


# -- Project information -----------------------------------------------------

project = "YesssSMS"
copyright = "2019, Florian Klien"
author = "Florian Klien"

# The full version, including alpha/beta/rc tags
version_file = open("../../YesssSMS/version.json")
version_info = version_file.read()
VERSION = json.loads(version_info)["version"]

release = VERSION

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["sphinx.ext.autodoc", "m2r2"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

source_suffix = [".rst", ".md"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"
# html_theme = "classic"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    "show_powered_by": False,
    "show_related": True,
    "note_bg": "#FFF59C",
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_sidebars = {
    "index": ["logo.html", "relations.html", "localtoc.html", "searchbox.html"],
    "**": [
        "logo.html",
        "localtoc.html",
        "relations.html",
        "sourcelink.html",
        "searchbox.html",
        # "hacks.html",
    ],
}


# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
html_show_sphinx = False
