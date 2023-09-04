import sys
import os
import argparse
from common import logger
from win32com.client import Dispatch


def listVersion(_dir):
    for path, dirs, files in os.walk(_dir):
        for file in files:
            if file.startswith("fmp-"):
                continue
            if not file.endswith(".dll"):
                continue
            filepath = os.path.join(path, file)
            info = Dispatch("Scripting.FileSystemObject")
            version = info.GetFileVersion(filepath)
            logger.debug("{} : {}".format(file, version))

def parse_args():
    parser = argparse.ArgumentParser("A pack and unpack tool for meta of vendor")
    parser.add_argument("-l", help="list", type=str)
    if len(sys.argv) > 1:
        args = parser.parse_args()
        if None != args.l:
            listVersion(args.l)
    else:
        parser.print_help()


if __name__ == "__main__":
    print("**************************************************")
    print("* module_version  - ver 1.0.0                       *")
    print("**************************************************")
    parse_args()
