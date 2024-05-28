import subprocess
import sys

main_path = "./src/main.py"
exe_name = "HW725UI"
upx_path = "./upx-4.2.4-win64"
def run_pyinstaller(icon_path):
    command = ["pyinstaller", "--onefile", "--windowed", "--icon=" + icon_path, "--name=" + exe_name, "--upx-dir=" + upx_path, main_path]
    try:
        subprocess.run(command, check=True)
        print("Completed.")
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {e}")


def main():
    if sys.platform.startswith('win'):
        icon_path = "src/images/ico.ico"
        run_pyinstaller(icon_path)


if __name__ == "__main__":
    main()
