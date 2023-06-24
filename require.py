import os
from time import sleep


def spelling(spell):
    for i in spell:
        print(i, end="")
        sleep(0.04)
    print()


def check_requirements():
    # os.system("python.exe -m pip install --upgrade pip")

    requirements = ('pytube', 'easygui', 'moviepy')

    for item in requirements:
        command_output = os.popen(f"{pip} list").read()

        if command_output.startswith("Package"):
            if item in command_output:
                pass

            else:
                spell = "Installing the requirements..."
                spelling(spell)
                os.system(f"{pip} install {item}")
                os.system(clear)

        else:
            raise Exception(
                "There is something wrong! Cannot install the required modules.")


if os.name == "nt":
    clear = "cls"
    pip = "pip"
else:
    clear = "clear"
    pip = "pip3"

check_requirements()
