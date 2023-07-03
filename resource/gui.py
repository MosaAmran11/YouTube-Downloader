from easygui import ynbox, diropenbox
from typing import Optional
import os


class GUI:
    def __init__(self, path: str) -> None:
        self.path = path

    def opendir(self, path: str) -> str:
        if os.name == 'nt':
            os.system(f'explorer "{path or self.path}"')
        else:
            os.system(f'nautilus "{path or self.path}"')

    def select_dir(self, initialdir: Optional[str] = None) -> str:
        path = diropenbox(title='Select Folder',
                          default=self.path) if not initialdir else diropenbox(title='Select Folder',
                                                                               default=initialdir)
        return path or self.path

    def ask_select_dir(self, message: str,
                       title='Select Folder') -> bool:
        return ynbox(title=title, msg=message)
