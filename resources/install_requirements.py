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


def run_command(*cmd):
    # Call the command with given arguments
    subprocess.run(
        [*cmd],
        capture_output=True
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


def main():
    try:
        upgrade_pip_command = [sys.executable, '-m',
                               'pip', 'install', '--upgrade', 'pip']
        requirements_path = os.path.join(
            os.path.dirname(__file__), 'requirements.txt')
        install_requirements_command = [sys.executable, '-m', 'pip',
                                        'install', '-r', requirements_path]
        subprocess.run(upgrade_pip_command)
        subprocess.run(install_requirements_command)
    except KeyboardInterrupt:
        print("Operation cancelled by user")
        exit()

    os.system(clear)
    spelling("All requirements are installed successfully.")
    sleep(2)


main()
