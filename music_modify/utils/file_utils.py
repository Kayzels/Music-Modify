"""General Utils for files. Not part of the main utils module
    due to import cycles.
    """

import os
import sys


def get_resource_path(relative_path: str) -> str:
    """Get the absolute path of the resource at the relative path sent in.

        Parameters
        ----------
        relative_path : str -
            The relative path of the resource.

        Returns
        -------
        str -
            The absolute path of the resource.
        """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)
