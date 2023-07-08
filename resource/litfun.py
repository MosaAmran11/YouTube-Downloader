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


def show_title(title, text: str = '{} title:\n', type: str = 'video'):
    spelling(
        text.format(type.capitalize()),
        end=None
    )
    if len(title) > 50:
        print(green, title, rset, sep='')


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
    print(rset, end='')
