"""Add this folder to the path, so that resources are accessible.
    """
import sys
from pathlib import Path

PATH_TO_ADD = str(Path(Path.cwd(), 'gui'))
sys.path.append(PATH_TO_ADD)
