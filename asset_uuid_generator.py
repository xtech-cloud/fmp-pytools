import sys
import os
import json
import argparse
import traceback
import hashlib
import uuid
from common import logger

def generate(_directory, _isGuid):
    if not os.path.exists(_directory):
        logger.error("{} not found".format(_directory))
        return

    bundle_meta_json_fullpath = os.path.join(_directory, "meta.json")
    if not os.path.exists(bundle_meta_json_fullpath):
        logger.error("meta.json of bundle not fount")
        return

    bundle_meta_dict = {
    }

    # 读取bundle/meta.json
    with open(bundle_meta_json_fullpath, mode="r", encoding="utf-8") as reader:
        bundle_meta_json_str = reader.read()
        reader.close()
        bundle_meta_dict = json.loads(bundle_meta_json_str)

    # 替换bundle的uuid
    if _isGuid:
        bundle_meta_dict["Uuid"] = str(uuid.uuid4())
    else:
        bundle_meta_dict["Uuid"] = os.path.basename(_directory)
    # 保存bundle/meta.json
    bundle_meta_json_str = json.dumps(bundle_meta_dict, ensure_ascii=False, indent=4)
    with open(bundle_meta_json_fullpath, mode="w", encoding="utf-8") as writer:
        writer.write(bundle_meta_json_str)
        writer.close()

    # 遍历包
    for content_dir in os.listdir(_directory):
        content_dir_fullpath = os.path.join(_directory, content_dir)
        if not os.path.isdir(content_dir_fullpath):
            continue
        if content_dir.startswith("_"):
            continue
        content_meta_json_fullpath = os.path.join(content_dir_fullpath, "meta.json")
        content_meta_dict = {
        }
        # 替换content的uuid
        if _isGuid:
            content_meta_dict["Uuid"] = str(uuid.uuid4())
        else:
            content_meta_dict["Uuid"] = os.path.basename(content_dir_fullpath)
        try:
            # 保存content/meta.json
            content_meta_json_str = json.dumps(content_meta_dict, ensure_ascii=False, indent=4)
            with open(content_meta_json_fullpath, mode="w", encoding="utf-8") as writer:
                writer.write(content_meta_json_str)
                writer.close()
        except Exception as e:
            logger.fatal(e)

def parse_args():
    parser = argparse.ArgumentParser("Generate the meta.json of bundle")
    parser.add_argument("-d", help="the directory of bundle", type=str, required=True)
    parser.add_argument("-g", help="use guid", action='store_true')
    if len(sys.argv) > 1:
        args = parser.parse_args()
        try:
            generate(args.d, args.g)
        except Exception as e:
            logger.fatal(e)
            traceback.print_exc()
        else:
            logger.info("success :)")
    else:
        parser.print_help()

if __name__ == "__main__":
    print("**************************************************")
    print("* asset_uuid_generator  - ver 1.0.0              *")
    print("**************************************************")
    parse_args()
