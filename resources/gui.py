from easygui import ynbox, diropenbox
from typing import Optional
import os


def opendir(path: str) -> int:
    return os.system(f'explorer "{path}"') if os.name == 'nt' else os.system(
        f'nautilus "{path}"')


def select_dir(initialdir: Optional[str] = None) -> str:
    return diropenbox(
        msg='Select Folder',
        title='Select Folder',
        default=initialdir)


def ask_select_dir(message: str,
                   title='Select Folder') -> bool:
    return ynbox(title=title, msg=message)


def ask_video_audio(
    message: str = "Video or Audio?",
    title: str = 'Select a subtype'
) -> bool:
    """
    return True for Video, False for Audio
    """
    ask = ynbox(msg=message, title=title, choices=(
        "[<F1>]Video", "[<F2>]Audio"),
        default_choice="[<F1>]Video",
        cancel_choice="[<F2>]Audio")
    return True if ask is None else ask
