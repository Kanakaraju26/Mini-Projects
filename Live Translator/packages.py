import subprocess
import sys


def install_package(package_name):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"Successfully installed {package_name}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package_name}. Error: {e}")


if __name__ == "__main__":
    packages_to_install = ["speechrecognition", "pygame", "pyaudio", "gtts", "googletrans", "dearpygui"]

    for package in packages_to_install:
        install_package(package)
