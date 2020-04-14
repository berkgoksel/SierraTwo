import argparse
import os
import platform
import subprocess
import sys
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--os", metavar="", required=True, type=str, help="Targeted operating system (Windows, Linux)")

    try:
        args = parser.parse_args()

    except:
        print("Missing arguments")
        sys.exit(0)

    builder(args.os)


def builder(dist):
    if dist.lower() == "windows":
        subprocess.run(["wine", "pyinstaller", "--onefile", "SierraTwo.py"])
        time.sleep(1)
        subprocess.run(["rm", "-rf", "build", "__pycache__", "SierraTwo.spec"])
        print("\nDone. Check 'dist' for your file")
        sys.exit(0)

    elif dist.lower() == "linux":
        subprocess.run(["pyinstaller", "--onefile", "SierraTwo.py"])
        time.sleep(1)
        subprocess.run(["rm", "-rf", "build", "__pycache__", "SierraTwo.spec"])
        print("\nDone. Check 'dist' for your file")
        sys.exit(0)

    else:
        print("Unsupported operating system")
        sys.exit(0)


if __name__ == "__main__":
    main()
