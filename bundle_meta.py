import sys
import os
import json
import argparse
import traceback
import hashlib
from common import logger


def getFileHash(_file):
    with open(_file, "rb") as fp:
        data = fp.read()
    return hashlib.md5(data).hexdigest()


def generate(_directory):
    if not os.path.exists(_directory):
        logger.error("{} not found".format(_directory))

    meta_json_fullpath = os.path.join(_directory, "meta.json")
    meta_dict = {
        "name": "",
        "summary": "",
        "labelS": [],
        "tagS": [],
        "resourceS": [],
        "summary_i18nS": {},
        "foreign_content_uuidS": [],
        "Uuid": "",
    }
    # 合并已存在的mate.json的部分属性
    if os.path.exists(meta_json_fullpath):
        with open(meta_json_fullpath, mode="r", encoding="utf-8") as reader:
            meta_json_str = reader.read()
            reader.close()
            exists_meta_dict = json.loads(meta_json_str)
            meta_dict["Uuid"] = exists_meta_dict["Uuid"]
            meta_dict["name"] = exists_meta_dict["name"]
            meta_dict["summary"] = exists_meta_dict["summary"]
            meta_dict["summary_i18nS"] = exists_meta_dict["summary_i18nS"]
    resourceS = []
    # 遍历包
    for subdir in os.listdir(_directory):
        subdir_fullpath = os.path.join(_directory, subdir)
        if not os.path.isdir(subdir_fullpath):
            continue
        if not subdir.startswith("_"):
            meta_dict["foreign_content_uuidS"].append(subdir)
        if subdir == "_resources":
            resources_fullpath = os.path.join(_directory, "_resources")
            for path, dirs, files in os.walk(os.path.join(_directory, "_resources")):
                for file in files:
                    if file.endswith(".hash"):
                        continue
                    file_fullpath = path + "/" + file
                    uri = os.path.relpath(file_fullpath, resources_fullpath)
                    resourceS.append(
                        {
                            "path": uri.replace("\\", "/"),
                            "hash": getFileHash(file_fullpath),
                            "size": os.path.getsize(file_fullpath),
                            "url": "",
                        }
                    )
    meta_dict["resourceS"] = resourceS
    meta_json = json.dumps(meta_dict, ensure_ascii=False, indent=4)
    # 保存meta.json
    with open(meta_json_fullpath, mode="w", encoding="utf-8") as writer:
        writer.write(meta_json)
        writer.close()

def parse_args():
    parser = argparse.ArgumentParser("Generate the meta.json of bundle")
    parser.add_argument("-d", help="the directory of bundle", type=str, required=True)
    if len(sys.argv) > 1:
        args = parser.parse_args()
        try:
            generate(args.d)
        except Exception as e:
            logger.fatal(e)
            traceback.print_exc()
        else:
            logger.info("success :)")
    else:
        parser.print_help()


if __name__ == "__main__":
    print("**************************************************")
    print("* bundle_meta  - ver 1.0.0                       *")
    print("**************************************************")
    parse_args()
