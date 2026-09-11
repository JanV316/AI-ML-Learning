"""
PassForge Application Entry Point (V6 CLI).
Run this script to launch the command-line interface or interactive menu.
"""

import sys
from passforge.cli import main

if __name__ == "__main__":
    main(sys.argv[1:])
