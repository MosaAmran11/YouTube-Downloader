from easygui import ynbox, diropenbox
from typing import Optional
import os


def opendir(path: str) -> str:
    if os.name == 'nt':
        os.system(f'explorer "{path}"')
    else:
        os.system(f'nautilus "{path}"')


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
    title: str = 'Select a type'
) -> bool:
    """
    return True for Video, False for Audio
    """
    ask = ynbox(msg=message, title=title, choices=(
        "[<F1>]Video", "[<F2>]Audio"),
        default_choice="[<F1>]Video",
        cancel_choice="[<F2>]Audio")
    if ask is None:
        return True
    else:
        return ask
    # return messagebox.askquestion(title, message)
