"""
Allow running the package as a module using `python -m tips`.
This delegates to the main entry point.
"""

from .main import main

if __name__ == "__main__":
    main()