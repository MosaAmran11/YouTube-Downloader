import os
from time import sleep


def spelling(spell):
    for i in spell:
        print(i, end="")
        sleep(0.04)
    print()


def check_requirements():
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

try:
    from pytube import YouTube
    import easygui
    from moviepy.editor import VideoFileClip

except ImportError:
    try:
        input("\n\nSome requirements will be installed to run this application.\nPress enter to continue...")
        print('\n\n')

        os.system(
            f'{pip} install -r {os.path.join(os.path.dirname(__file__), "requirements.txt")}')

    except KeyboardInterrupt:
        print("Operation cancelled by user")
        exit()

    except:
        check_requirements()
