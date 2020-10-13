"""Add this folder to the path, so that resources are accessible.
    """
import sys
from pathlib import Path
from utils import file_utils

# PATH_TO_ADD = str(Path(Path.cwd(), 'gui'))
# sys.path.append(PATH_TO_ADD)
relative_path = str(Path('music_modify', 'gui'))
path_to_add = file_utils.get_resource_path(relative_path)
sys.path.append(path_to_add)

# from gui import resources_rc
