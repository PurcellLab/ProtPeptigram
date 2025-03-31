#!/usr/bin/env python3
"""
Script to set up the Sphinx documentation directory structure for ProtPeptigram.
Run this script from the root of your project repository.
"""
import os
import shutil

def setup_docs_structure():
    """Create the necessary directories for Sphinx documentation."""
    # Create main docs directory if it doesn't exist
    if not os.path.exists('docs'):
        os.makedirs('docs')
    
    # Create modules subdirectory
    if not os.path.exists('docs/modules'):
        os.makedirs('docs/modules')
    
    # Create _static and _templates directories
    for dir_name in ['_static', '_templates', '_build']:
        if not os.path.exists(f'docs/{dir_name}'):
            os.makedirs(f'docs/{dir_name}')
    
    print("✅ Created docs directory structure")
    
    # If docs/html exists, back it up
    if os.path.exists('docs/html'):
        print("⚠️  docs/html directory already exists")
        backup_dir = 'docs/html_backup'
        if os.path.exists(backup_dir):
            shutil.rmtree(backup_dir)
        shutil.move('docs/html', backup_dir)
        print(f"✅ Backed up existing docs/html to {backup_dir}")
    
    print("\nDocs setup complete. You can now place the documentation files in their respective directories.")
    print("\nTo build the documentation locally, run:")
    print("  cd docs")
    print("  sphinx-build -b html . _build/html")

if __name__ == '__main__':
    setup_docs_structure()