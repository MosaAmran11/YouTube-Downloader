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


def show_title(title, type: str = 'video', text: str = '{} title:'):
    print(
        text.format(type.capitalize())
    )
    if len(title) > 50:
        print(green, title, rset, sep='')
    else:
        print(green, end='')
        print(title)
        print(rset, end='')


def exit_message():
    print(yellow, 'Thanks for using our YouTube Downloader.', rset)
    print(cyan, '\tMADE BY MAA\t'.center(50, "#"), rset)
    sleep(0.8)
    print(f'{red}Exiting from downloader...{rset}')
    sleep(0.8)


def show_download_message(media_type='video', text=''):
    print(cyan, end='')
    print(
        f'Downloading the {media_type.capitalize()} {text}',
        'It may take a long time. Please wait...',
        sep='\n'
    )
    print(rset, end='')
