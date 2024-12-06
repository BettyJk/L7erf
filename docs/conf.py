# See https://docs.readthedocs.io/en/stable/config-file/v2.html for details

# Required
version: 2

# Set the OS, Python version and other tools you might need
build:
  os: ubuntu-22.04
  tools:
    python: "3.10"

# Build documentation in the "docs/" directory with Sphinx
sphinx:
  builder: html
  configuration: conf.py
  # You can configure Sphinx to use a different builder, for instance use the dirhtml builder for simpler URLs
  # builder: "dirhtml"
  # Fail on all warnings to avoid broken references
  # fail_on_warning: true

# Optionally build your docs in additional formats such as PDF and ePub
#formats:
 # - pdf
  # - epub

# Optional but recommended, declare the Python requirements required
# to build your documentation
# See https://docs.readthedocs.io/en/stable/guides/reproducible-builds.html
python:
  install:
    - requirements: requirements.in
