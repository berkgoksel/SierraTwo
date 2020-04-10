import argparse
import cython
import platform
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--os", metavar="", required=True, type=str, help="Targeted operating system (Windows, Linux)")

    try:
        args = parser.parse_args()

    except:
        print("Missing arguments")
        sys.exit(0)

    builder(args.os)


def builder(os):
    if os.lower() == "windows":
        subprocess.run(["wine", "python", "pyinstaller", "--onefile", "../SierraTwo.py"])
        subprocess.run(["mv", "../__pycache__/", "."])
        print("\nDone. Check 'dist' for your file")
        sys.exit(0)

    elif os.lower() == "linux":
        subprocess.run(["pyinstaller", "--onefile", "../SierraTwo.py"])
        subprocess.run(["mv", "../__pycache__/", "."])
        print("\nDone. Check 'dist' for your file")
        sys.exit(0)
    
    else:
        print("Unsupported operating system")
        sys.exit(0)


if __name__ == "__main__":
    main()
