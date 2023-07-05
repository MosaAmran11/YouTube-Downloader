import os
import subprocess
import sys
from time import sleep


requirements = ('pytube', 'easygui', 'moviepy')
clear = "cls" if os.name == "nt" else "clear"
path = os.path.dirname(__file__)


def spelling(spell):
    for i in spell:
        print(i, end="")
        sleep(0.04)
    print()


def run_command(*CMD):
    subprocess.run(
        [*CMD],
        # capture_output=True
    )


def check_requirements():
    os.system(clear)
    command_output = os.popen(f"{sys.executable} -m pip list").read()
    if command_output.startswith("Package"):
        for pack in requirements:
            os.system(clear)
            # Check if the Package name within the list
            if pack not in command_output:
                spelling("Installing the requirements...")
                run_command(sys.executable,
                            '-m',
                            'pip',
                            'install',
                            pack)
    else:
        print(
            "There is something wrong! Cannot install the required modules.")
        exit()


def install(package, *packages):
    if type(package) is list or type(package) is tuple:
        for pack in package:
            run_command(sys.executable,
                        '-m',
                        'pip',
                        'install',
                        pack)
    elif type(package) is str:
        # If input is a requirements file
        if os.path.isfile(package):
            run_command(sys.executable,
                        '-m',
                        'pip',
                        'install',
                        '-r',
                        package)
        else:
            run_command(sys.executable,
                        '-m',
                        'pip',
                        'install',
                        package)
    if packages:
        for pack in packages:
            run_command(sys.executable,
                        '-m',
                        'pip',
                        'install',
                        pack)


try:
    try:
        from pytube import YouTube
        import easygui
        from moviepy.editor import VideoFileClip
    except ImportError:
        os.system(clear)
        print("Some requirements will be installed to run this application.")
        input("Press enter to continue...")
        os.system(clear)

        requirements = os.path.join(path, 'requirements.txt')
        spelling("Installing the requirements...")
        install(requirements)

    except:
        check_requirements()
except KeyboardInterrupt:
    print("Operation cancelled by user")
    exit()

spelling("All requirements are installed successfully.")
sleep(2)
os.system(clear)
