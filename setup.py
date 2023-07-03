import os
from pathlib import Path
from win32com.client import Dispatch


def create_shortcut(source, iconfile, destination):
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortcut(destination)
    shortcut.TargetPath = source
    shortcut.IconLocation = iconfile
    shortcut.WindowStyle = 7
    shortcut.Save()


def generate_bat_file():
    app_directory = os.getcwd()[:-5]  # Get the current directory path
    # Get the Anaconda base environment path
    anaconda_path = os.path.expanduser("~")+"\\anaconda3"

    bat_content = f"""
    @echo off
    call "{anaconda_path}\\Scripts\\activate.bat" base
    cd "{app_directory}"
    call python game.py
    call python plot_progress.py
    call conda deactivate
    """

    with open("../launch.bat", "w") as bat_file:
        bat_file.write(bat_content)


def generate_setup():
    # Create the bat file
    generate_bat_file()

    # Create the desktop shortcut
    desktop = Path(os.path.join(os.path.join(
        os.environ['USERPROFILE']), 'OneDrive\Desktop'))
    shortcut_path = desktop / "YourApp.lnk"
    # print(f'''
    #       -----------------------------
    #       {shortcut_path}
    #       -----------------------------
    #       ''')
    create_shortcut(os.getcwd()[:-5]+"\\launch.bat",
                    os.getcwd()[:-5]+"\\app_icon.ico", str(shortcut_path))

    print("Setup completed successfully.")


generate_setup()
