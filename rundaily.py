import subprocess
import os

def main():
    """Check if datacollection.py is running. If it is not, start it."""

    p = subprocess.Popen(['pgrep', '-f', 'datacollection.py'], stdout=subprocess.PIPE)
    out, err = p.communicate()

    if len(out.strip()) == 0:
        os.system("python datacollection.py")

if __name__ == '__main__':
    main()