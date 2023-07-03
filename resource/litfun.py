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
            print(i, '', sep=bet or '', end='')
            sleep(delay)
        print(sep=sep or '', end='')
    print(sep='', end=end or '')


def show_title(title):
    spelling(
        "The title of video is:\n",
        green,
        title
    )
    print(rset, sep='', end='')


def exit_message():
    spelling(f'{yellow}\nThanks for using our YouTube Downloader.{rset}')
    spelling(f'{cyan}\tMADE BY MAA\t{rset}'.center(50, "#"))
    sleep(0.8)
    spelling(f'{red}Exiting from downloader...{rset}')
    sleep(0.8)


def show_download_message(media_type='video', text=''):
    spelling(
        f'{cyan}\nDownloading the {media_type.capitalize()} {text}\n',
        'It may take a long time. Please wait...'
    )
    print(rset)
