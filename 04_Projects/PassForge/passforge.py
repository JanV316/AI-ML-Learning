"""
PassForge Execution Wrapper.
Delegates execution to passforge.cli module.
"""

import sys
from passforge.cli import main

if __name__ == "__main__":
    main(sys.argv[1:])
