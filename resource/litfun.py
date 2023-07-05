"""
Literal functions module provides functions
to display messages.
"""
from time import sleep
from vars import *


def spelling(
        *spells: str,
        bet: str | None = None,
        sep: str | None = '',
        end: str | None = '\n',
        delay: float = 0.04
) -> None:
    for spell in spells:
        for i in spell:
            print(i, bet or "", sep='', end='')
            sleep(delay)
        print(sep or "", sep='', end='')
    print(end or "", sep='', end='')


def show_title(title, type: str = 'video'):
    spelling(
        f"The title of {type.capitalize()} is:\n",
        green,
        title,
        sep=None
    )
    print(rset, end='')


def exit_message():
    spelling(yellow, 'Thanks for using our YouTube Downloader.', rset)
    spelling(cyan, '\tMADE BY MAA\t'.center(50, "#"), rset)
    sleep(0.8)
    spelling(f'{red}Exiting from downloader...{rset}')
    sleep(0.8)


def show_download_message(media_type='video', text=''):
    print(cyan, end='')
    spelling(
        f'Downloading the {media_type.capitalize()}{text}',
        'It may take a long time. Please wait...',
        sep='\n'
    )
    print(rset)
