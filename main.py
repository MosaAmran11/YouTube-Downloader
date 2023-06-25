from os import system
from time import sleep
from yd import YD

system(YD.clear)
url = input("\nEnter a YouTube Link => ")
yt = YD(url)

yt.get_title()
sleep(1)
yt.streams_menu()
yt.select_folder()
yt.download()
yt.openFile()
yt.exit_msg
