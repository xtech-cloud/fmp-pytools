import sys
import os
import json
import argparse
import traceback
import hashlib
import shutil
from common import logger


def getFileHash(_file):
    with open(_file, "rb") as fp:
        data = fp.read()
    return hashlib.md5(data).hexdigest()


def make(_directory):
    if not os.path.exists(_directory):
        logger.error("{} not found".format(_directory))

    output_dir = _directory + ".mc"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    entryS = []
    index = 0
    for dirpath, dirnames, filenames in os.walk(_directory):
        for filepath in filenames:
            index = index + 1
            filename, extension = os.path.splitext(filepath)
            entry = {
                "thumbnail": "thumbnail-{}.jpg".format(index),
                "file": "{}.jpg".format(index),
                "summary": filename,
            }
            entryS.append(entry)
            file_src = os.path.join(dirpath, filepath)
            file_dest = os.path.join(output_dir, entry["file"])
            thumbnail_dest = os.path.join(output_dir, entry["thumbnail"])
            shutil.copy(file_src, file_dest)
            shutil.copy(file_src, thumbnail_dest)
    schema = {}
    schema["entryS"] = entryS
    schema_json = json.dumps(schema, ensure_ascii=False, indent=4)
    # 保存meta.json
    with open(os.path.join(output_dir, "meta.json"), mode="w", encoding="utf-8") as writer:
        writer.write(schema_json)
        writer.close()


def parse_args():
    parser = argparse.ArgumentParser("Make MediaCenter")
    parser.add_argument("-d", help="the directory", type=str, required=True)
    if len(sys.argv) > 1:
        args = parser.parse_args()
        try:
            make(args.d)
        except Exception as e:
            logger.fatal(e)
            traceback.print_exc()
        else:
            logger.info("success :)")
    else:
        parser.print_help()


if __name__ == "__main__":
    print("**************************************************")
    print("* MediaCenter Make  - ver 1.0.0                  *")
    print("**************************************************")
    parse_args()
