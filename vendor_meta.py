import sys
import os
import shutil
import argparse
import base64
import json
from xml.etree import ElementTree as ET
from xml.dom import minidom
from common import logger


def strFromBase64Str(_str: str):
    """
    从base64字符转换为明文字符
    """
    # 解码base64
    bytes_value = _str.encode(encoding="utf-8")
    decoded_bytes = base64.b64decode(bytes_value)
    # byte[] to str
    return decoded_bytes.decode(encoding="utf-8")


def strToBase64Str(_str: str):
    """
    将明文字符转换为base64字符
    """
    # 编码base64
    bytes_value = _str.encode(encoding="utf-8")
    encoded_bytes = base64.b64encode(bytes_value)
    # 保存 dependency.xml
    return encoded_bytes.decode(encoding="utf-8")


def _prettifyXML(_schema):
    rough_string = ET.tostring(_schema, "utf-8")
    reparsed = minidom.parseString(rough_string)
    reparsed.toprettyxml(indent="\t")
    return reparsed.toprettyxml(indent="\t")


def strFromJsonDict(_dict: dict):
    json_str = json.dumps(_dict, ensure_ascii=False, indent=4)
    return json_str


def read_file(_file):
    content = ""
    with open(_file, mode="r", encoding="utf-8") as reader:
        content = reader.read()
        reader.close()
    return content


def write_file(_file, _content):
    with open(_file, mode="w", encoding="utf-8") as writer:
        writer.write(_content)
        writer.close()


def unpack(_file, _overwrite):
    if not os.path.exists(_file):
        logger.error("{} not found".format(_file))

    output_dir_root = os.path.join(os.path.dirname(_file), ".meta")
    if os.path.exists(output_dir_root):
        if not _overwrite:
            logger.error(
                "the directory {} exists, please delete it".format(output_dir_root)
            )
            sys.exit(1)
        else:
            shutil.rmtree(output_dir_root)
    os.makedirs(output_dir_root, exist_ok=True)

    root_schema = {}
    with open(_file, mode="r", encoding="utf-8") as reader:
        content = reader.read()
        reader.close()
        root_schema = json.loads(content)
    """
    保存vendor.json
    """
    vendor_json_file_fullpath = os.path.join(output_dir_root, "vendor.json")
    vendor_schema = {
        "Uuid": root_schema["Uuid"],
        "Name": root_schema["Name"],
        "Display": root_schema["Name"],
        "SkinSplashBackground": root_schema["Name"],
        "SkinSplashSlogan": root_schema["Name"],
        "GraphicsFPS": root_schema["GraphicsFPS"],
        "GraphicsQuality": root_schema["GraphicsQuality"],
        "GraphicsPixelResolution": root_schema["GraphicsPixelResolution"],
        "GraphicsReferenceResolutionWidth": root_schema[
            "GraphicsReferenceResolutionWidth"
        ],
        "GraphicsReferenceResolutionHeight": root_schema[
            "GraphicsReferenceResolutionHeight"
        ],
        "GraphicsReferenceResolutionMatch": root_schema[
            "GraphicsReferenceResolutionMatch"
        ],
        "Application": root_schema["Application"],
    }
    vendor_json_str = strFromJsonDict(vendor_schema)
    write_file(vendor_json_file_fullpath, vendor_json_str)
    """
    保存dependency.xml
    """
    dependency_xml_file_fullpath = os.path.join(output_dir_root, "dependency.xml")
    dependency_base64_str = root_schema["DependencyConfig"]
    dependency_xml_str = strFromBase64Str(dependency_base64_str)
    # 保存 dependency.xml
    write_file(dependency_xml_file_fullpath, dependency_xml_str)
    """
    保存update.xml
    """
    update_xml_file_fullpath = os.path.join(output_dir_root, "update.xml")
    update_base64_str = root_schema["UpdateConfig"]
    update_xml_str = strFromBase64Str(root_schema["UpdateConfig"])
    # 保存 update.xml
    write_file(update_xml_file_fullpath, update_xml_str)
    """
    保存bootloader.xml
    """
    bootloader_xml_file_fullpath = os.path.join(output_dir_root, "bootloader.xml")
    bootloader_base64_str = root_schema["BootloaderConfig"]
    bootloader_xml_str = strFromBase64Str(bootloader_base64_str)
    # 保存 bootloader.xml
    write_file(bootloader_xml_file_fullpath, bootloader_xml_str)
    """
    保存configs
    """
    output_dir_configs = os.path.join(output_dir_root, "configs")
    os.makedirs(output_dir_configs, exist_ok=True)
    for pair in root_schema["ModuleConfigS"].items():
        config_xml_file_fullpath = os.path.join(output_dir_configs, pair[0] + ".xml")
        config_base64_str = pair[1]
        config_xml_str = strFromBase64Str(config_base64_str)
        # 保存 config.xml
        write_file(config_xml_file_fullpath, config_xml_str)
    """
    保存catalogs
    """
    output_dir_catalogs = os.path.join(output_dir_root, "catalogs")
    os.makedirs(output_dir_catalogs, exist_ok=True)
    for pair in root_schema["ModuleCatalogS"].items():
        catalog_json_file_fullpath = os.path.join(
            output_dir_catalogs, pair[0] + ".json"
        )
        catalog_base64_str = pair[1]
        catalog_json_str = strFromBase64Str(catalog_base64_str)
        # 保存 catalog.json
        write_file(catalog_json_file_fullpath, catalog_json_str)
    """
    保存themes
    """
    output_dir_themes = os.path.join(output_dir_root, "themes")
    os.makedirs(output_dir_themes, exist_ok=True)
    for pair in root_schema["ModuleThemeS"].items():
        theme_json_file_fullpath = os.path.join(output_dir_themes, pair[0] + ".json")
        theme_dict = pair[1]
        theme_json = strFromJsonDict(pair[1])
        # 保存 theme.json
        write_file(theme_json_file_fullpath, theme_json)


def pack(_dir, _overwrite):
    input_dir_root = _dir
    if not os.path.exists(input_dir_root):
        logger.error("the directory {} not found".format(input_dir_root))
        sys.exit(1)
    input_dir_configs = os.path.join(input_dir_root, "configs")
    input_dir_catalogs = os.path.join(input_dir_root, "catalogs")
    input_dir_themes = os.path.join(input_dir_root, "themes")
    vendor_schema = {}
    """
    读取vendor.json
    """
    vendor_json_file_fullpath = os.path.join(input_dir_root, "vendor.json")
    if not os.path.exists(vendor_json_file_fullpath):
        logger.error("the file {} not found".format(vendor_json_file_fullpath))
        sys.exit(1)
    with open(vendor_json_file_fullpath, mode="r", encoding="utf-8") as reader:
        vendor_json = reader.read()
        vendor_schema = json.loads(vendor_json)
        reader.close()
    """
    读取dependency.xml
    """
    dependency_xml_file_fullpath = os.path.join(input_dir_root, "dependency.xml")
    dependency_xml_str = read_file(dependency_xml_file_fullpath)
    dependency_base64_str = strToBase64Str(dependency_xml_str)
    vendor_schema["DependencyConfig"] = dependency_base64_str
    """
    读取update.xml
    """
    update_xml_file_fullpath = os.path.join(input_dir_root, "update.xml")
    update_xml_str = read_file(update_xml_file_fullpath)
    update_base64_str = strToBase64Str(update_xml_str)
    vendor_schema["UpdateConfig"] = update_base64_str
    """
    读取bootloader.xml
    """
    bootloader_xml_file_fullpath = os.path.join(input_dir_root, "bootloader.xml")
    bootloader_xml_str = read_file(bootloader_xml_file_fullpath)
    bootloader_base64_str = strToBase64Str(bootloader_xml_str)
    vendor_schema["BootloaderConfig"] = bootloader_base64_str
    """
    读取configs
    """
    vendor_schema["ModuleConfigS"] = {}
    input_dir_configs = os.path.join(input_dir_root, "configs")
    for file_name in os.listdir(input_dir_configs):
        if not file_name.endswith(".xml"):
            continue
        config_xml_file_fullpath = os.path.join(input_dir_configs, file_name)
        config_xml_str = read_file(config_xml_file_fullpath)
        config_base64_str = strToBase64Str(config_xml_str)
        module_name = file_name[:len(file_name)-len(".xml")]
        vendor_schema["ModuleConfigS"][module_name] = config_base64_str
    """
    读取catalogs
    """
    vendor_schema["ModuleCatalogS"] = {}
    input_dir_catalogs = os.path.join(input_dir_root, "catalogs")
    for file_name in os.listdir(input_dir_catalogs):
        if not file_name.endswith(".json"):
            continue
        catalog_json_file_fullpath = os.path.join(input_dir_catalogs, file_name)
        catalog_json_str = read_file(catalog_json_file_fullpath)
        catalog_base64_str = strToBase64Str(catalog_json_str)
        module_name = file_name[:len(file_name)-len(".json")]
        vendor_schema["ModuleCatalogS"][module_name] = catalog_base64_str
    """
    读取themes
    """
    vendor_schema["ModuleThemeS"] = {}
    input_dir_themes = os.path.join(input_dir_root, "themes")
    for file_name in os.listdir(input_dir_themes):
        if not file_name.endswith(".json"):
            continue
        theme_json_file_fullpath = os.path.join(input_dir_themes, file_name)
        theme_json_str = read_file(theme_json_file_fullpath)
        theme_json_dict = json.loads(theme_json_str)
        module_name = file_name[:len(file_name)-len(".json")]
        vendor_schema["ModuleThemeS"][module_name] = theme_json_dict
    """
    保存meta.json
    """
    output_file = os.path.join(os.path.dirname(_dir), "meta.json")
    vendor_json = json.dumps(vendor_schema, ensure_ascii=False, indent=4)
    write_file(output_file, vendor_json)


def parse_args():
    parser = argparse.ArgumentParser("A pack and unpack tool for meta of vendor")
    parser.add_argument("-x", help="extract files from a meta.json", type=str)
    parser.add_argument("-c", help="create a new meta.json", type=str)
    parser.add_argument("-y", help="is overwrite", action="store_true")
    if len(sys.argv) > 1:
        args = parser.parse_args()
        if None != args.x:
            unpack(args.x, args.y)
        elif None != args.c:
            pack(args.c, args.y)
    else:
        parser.print_help()


if __name__ == "__main__":
    txt = "ab.txt"
    parse_args()
