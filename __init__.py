# import peptigram
# ProtPeptigram/__init__.py
# import sys
# import os

# # Add the parent directory to the path so we can import main.py from root
# sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# try:
#     from main import main
# except ImportError:
#     # If main.py is not in root, define a placeholder
#     def main():
#         print("Main function not found")
#         return 1

# __all__ = ['main']