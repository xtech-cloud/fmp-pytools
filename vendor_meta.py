import sys
import os
import shutil
import argparse
import base64
import json
from xml.etree import ElementTree as ET
from xml.dom import minidom
from common import logger

def prettifyXML(_schema):
    rough_string = ET.tostring(_schema, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    reparsed.toprettyxml(indent="\t")
    return reparsed.toprettyxml(indent="\t")

def prettifyJson(_schema):
    return json.dumps(_schema, ensure_ascii=True, indent=4)

def write(_file, _content):
    with open(_file, mode='w', encoding="utf-8") as writer:
        writer.write(_content)
        writer.close()


def unpack(_file, _overwrite):
    if not os.path.exists(_file):
        logger.error("{} not found".format(_file))

    output_dir_root = os.path.join(os.path.dirname(_file), ".meta")
    if os.path.exists(output_dir_root):
        if not _overwrite:
            logger.error("the directory {} exists, please delete it".format(output_dir_root))
            sys.exit(1)
        else:
            shutil.rmtree(output_dir_root)
    output_dir_configs = os.path.join(output_dir_root, "configs")
    output_dir_catalogs = os.path.join(output_dir_root, "catalogs")
    output_dir_themes = os.path.join(output_dir_root, "themes")
    os.makedirs(output_dir_configs, exist_ok=True)
    os.makedirs(output_dir_catalogs, exist_ok=True)
    os.makedirs(output_dir_themes, exist_ok=True)

    with open(_file, mode='r', encoding="utf-8") as reader:
        content = reader.read()
        schema = json.loads(content)
        """
        保存vendor.json
        """
        vendor_json_file_fullpath = os.path.join(output_dir_root, "vendor.json")
        vendor_schema = {
                "Uuid": schema["Uuid"],
                "Name": schema["Name"],
                "Display": schema["Name"],
                "SkinSplashBackground": schema["Name"],
                "SkinSplashSlogan": schema["Name"],
                "GraphicsFPS": schema["GraphicsFPS"],
                "GraphicsQuality": schema["GraphicsQuality"],
                "GraphicsPixelResolution": schema["GraphicsPixelResolution"],
                "GraphicsReferenceResolutionWidth": schema["GraphicsReferenceResolutionWidth"],
                "GraphicsReferenceResolutionHeight": schema["GraphicsReferenceResolutionHeight"],
                "GraphicsReferenceResolutionMatch": schema["GraphicsReferenceResolutionMatch"],
                "Application": schema["Application"],
                }
        vendor_json = prettifyJson(vendor_schema)
        write(vendor_json_file_fullpath, vendor_json)
        """
        保存dependency.xml
        """
        dependency_xml_file_fullpath = os.path.join(output_dir_root, "dependency.xml")
        dependency_base64 = schema["DependencyConfig"]
        # 解码base64
        dependency_xml = base64.b64decode(dependency_base64)
        # 保存 dependency.xml
        write(dependency_xml_file_fullpath, str(dependency_xml, encoding="utf-8"))
        """
        保存update.xml
        """
        update_xml_file_fullpath = os.path.join(output_dir_root, "update.xml")
        update_base64 = schema["UpdateConfig"]
        # 解码base64
        update_xml = base64.b64decode(update_base64)
        # 保存 update.xml
        write(update_xml_file_fullpath, str(update_xml, encoding="utf-8"))
        """
        保存bootloader.xml
        """
        bootloader_xml_file_fullpath = os.path.join(output_dir_root, "bootloader.xml")
        bootloader_base64 = schema["BootloaderConfig"]
        # 解码base64
        bootloader_xml = base64.b64decode(bootloader_base64)
        # 保存 bootloader.xml
        write(bootloader_xml_file_fullpath, str(bootloader_xml, encoding="utf-8"))
        """
        保存configs
        """
        for pair in schema["ModuleConfigS"].items():
            config_xml_file_fullpath = os.path.join(output_dir_configs, pair[0]+".xml")
            config_base64 = pair[1]
            # 解码base64
            config_xml = base64.b64decode(config_base64)
            # 保存 config.xml
            write(config_xml_file_fullpath, str(config_xml, encoding="utf-8"))
        """
        保存catalogs
        """
        for pair in schema["ModuleCatalogS"].items():
            catalog_json_file_fullpath = os.path.join(output_dir_catalogs, pair[0]+".json")
            catalog_base64 = pair[1]
            # 解码base64
            catalog_json = base64.b64decode(catalog_base64)
            # 保存 catalog.json
            write(catalog_json_file_fullpath, str(catalog_json, encoding="utf-8"))
        """
        保存themes
        """
        for pair in schema["ModuleThemeS"].items():
            theme_json_file_fullpath = os.path.join(output_dir_themes, pair[0]+".json")
            theme_json = prettifyJson(pair[1])
            # 保存 theme.json
            write(theme_json_file_fullpath, theme_json)

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
    with open(dependency_xml_file_fullpath, mode="r", encoding="utf-8") as reader:
        dependency_xml = reader.read()
        reader.close()
        dependency_base64 = base64.b64encode(str.encode(dependency_xml, encoding="utf-8"))
        vendor_schema["DependencyConfig"] = str(dependency_base64, encoding="utf-8")
    output_file = os.path.join(os.path.dirname(_dir), "meta.json")
    """
    读取update.xml
    """
    update_xml_file_fullpath = os.path.join(input_dir_root, "update.xml")
    with open(update_xml_file_fullpath, mode="r", encoding="utf-8") as reader:
        update_xml = reader.read()
        reader.close()
        update_base64 = base64.b64encode(str.encode(update_xml, encoding="utf-8"))
        vendor_schema["UpdateConfig"] = str(update_base64, encoding="utf-8")
    """
    读取bootloader.xml
    """
    bootloader_xml_file_fullpath = os.path.join(input_dir_root, "bootloader.xml")
    with open(bootloader_xml_file_fullpath, mode="r", encoding="utf-8") as reader:
        bootloader_xml = reader.read()
        reader.close()
        bootloader_base64 = base64.b64encode(str.encode(bootloader_xml, encoding="utf-8"))
        vendor_schema["BootloaderConfig"] = str(bootloader_base64, encoding="utf-8")
    """
    保存meta.json
    """
    output_file = os.path.join(os.path.dirname(_dir), "meta.json")
    vendor_json = json.dumps(vendor_schema, ensure_ascii=True, indent=4)
    write(output_file, vendor_json)

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
    parse_args()

