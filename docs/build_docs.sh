#!/bin/bash
# Script to build documentation using pdoc

# Install pdoc if not already installed
pip install pdoc3

# Install the package in development mode
pip install -e ..

# Create output directory
mkdir -p _build/html

# Generate HTML documentation using pdoc
pdoc --html --output-dir _build/html ../ProtPeptigram

# If we already have some HTML content, preserve it
if [ -d "html" ]; then
  cp -r html/* _build/html/
fi

echo "Documentation built successfully in _build/html"