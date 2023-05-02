"""
Python app to read a blog.yaml and generate a blog file structure
and index.md markdown file from a template
"""

import os
import pathlib
import argparse
import oyaml as yaml
import shutil
import readtime


TEMPLATE_FILE = "module.md"
INDEX_TEMPLATE = "index.template"
INDEX_YAML = "index.yml"
MODULE_FILE = "module.yml"

MEDIA_FOLDER = "media"
INCLUDES_FOLDER = "includes"
SOURCE_FOLDER = "source"
RESOURCES_FOLDER = "resources"

INPUT_FOLDER = None
OUTPUT_FOLDER = None


def set_key_value(units, unit, key):
    """Get ket value"""
    unit[key] = unit.get(key, units['module'][key])


def delete_output_folder():
    """Reset the output folder"""

    if os.path.exists(OUTPUT_FOLDER):
        shutil.rmtree(os.path.join(OUTPUT_FOLDER))

    pathlib.Path(OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)


def copy_source_files():
    """Copy project assets to MS Learning format"""

    pathlib.Path(os.path.join(OUTPUT_FOLDER, INCLUDES_FOLDER)
                 ).mkdir(parents=True, exist_ok=True)
    for filename in os.listdir(os.path.join(INPUT_FOLDER, SOURCE_FOLDER)):
        if filename.endswith(".md"):
            src = os.path.join(INPUT_FOLDER, SOURCE_FOLDER, filename)
            dst = os.path.join(OUTPUT_FOLDER, INCLUDES_FOLDER, filename)
            shutil.copy2(src, dst)

    src = os.path.join(INPUT_FOLDER, MEDIA_FOLDER)
    dst = os.path.join(OUTPUT_FOLDER, MEDIA_FOLDER)
    shutil.copytree(src, dst)

    src = os.path.join(INPUT_FOLDER, RESOURCES_FOLDER)
    dst = os.path.join(OUTPUT_FOLDER, RESOURCES_FOLDER)
    shutil.copytree(src, dst)


def get_module_key_value(units, key):
    """get key from module"""
    return units.get(key, units['module'][key])


def create_index_yml(root):
    """Create the index.yml file"""

    index = {}
    index["uid"] = root['module']['uid_root']

    index["metadata"] = {}
    index["metadata"]["title"] = get_module_key_value(root, 'title')
    index["metadata"]["description"] = get_module_key_value(
        root, 'description')
    index["metadata"]["author"] = get_module_key_value(root, 'author')
    index["metadata"]["ms.date"] = get_module_key_value(root, 'date')
    index["metadata"]["ms.author"] = get_module_key_value(root, 'author')
    index["metadata"]["ms.topic"] = get_module_key_value(root, 'topic')
    index["metadata"]["ms.prod"] = get_module_key_value(root, 'prod')
    index["metadata"]["ms.custom"] = get_module_key_value(root, 'custom')

    index["title"] = get_module_key_value(root, 'title')
    index["summary"] = get_module_key_value(root, 'summary')
    index["abstract"] = get_module_key_value(root, 'abstract')
    index["prerequisites"] = get_module_key_value(root, 'prerequisites')
    index["levels"] = get_module_key_value(root, 'levels')

    index["badge"] = {}
    index["badge"]["uid"] = get_module_key_value(root, 'uid_root') + ".badge"

    index["roles"] = get_module_key_value(root, 'roles')
    index["products"] = get_module_key_value(root, 'products')
    index["subjects"] = get_module_key_value(root, 'subjects')

    index["units"] = []

    for unit in root['module']['units']:
        uid = root['module']['uid_root'] + "." + \
            unit["unit"].lower().replace(' ', '-').split(".")[0]
        index["units"].append(uid)

    filename = os.path.join(OUTPUT_FOLDER, INDEX_YAML)
    with open(filename, 'w', encoding='utf8') as file:
        file.write("### YamlMime:Module\n")
        yaml.dump(index, file)


def create_module_yml(root):
    """Create the module.yml file"""
    for unit in root['module']['units']:

        markdown_filename = unit.get('unit')
        markdown_filename = os.path.join(
            INPUT_FOLDER, SOURCE_FOLDER, markdown_filename)

        if os.path.isfile(markdown_filename):
            text = open(markdown_filename, encoding='utf8').read()

            if markdown_filename.endswith(".yml"):

                question = yaml.load(text, Loader=yaml.Loader)
                unit['quiz'] = question

            if unit.get('durationInMinutes') is None:
                result = readtime.of_text(text)
                minutes = result.text.split(" ")[0]
                unit['durationInMinutes'] = minutes

        else:
            print("Unit file .md or .yml not found for: " + unit['unit'])
            exit()


        unit_file = unit.get('unit').split(".")[0] + ".yml"
        filename = os.path.join(OUTPUT_FOLDER, unit_file)

        output = {}
        output["uid"] = root['module']['uid_root'] + "." + unit.get('unit').lower().replace(' ', '-').split(".")[0]
        output["title"] = unit.get('title')
        output["metadata"] = {}
        output["metadata"]["title"] = unit.get('title')
        output["metadata"]["description"] = unit.get('description')
        output["metadata"]["ms.date"] = get_module_key_value(root, 'date')
        output["metadata"]["author"] = get_module_key_value(root, 'author')
        output["metadata"]["ms.author"] = get_module_key_value(root, 'author')
        output["metadata"]["ms.topic"] = get_module_key_value(root, 'topic')
        output["metadata"]["ms.prod"] = get_module_key_value(root, 'prod')
        output["metadata"]["ms.custom"] = get_module_key_value(root, 'custom')
        output["durationInMinutes"] = unit.get('durationInMinutes')
        if unit.get('quiz') is not None:
            output["quiz"] = unit.get('quiz')
        else:
            output["content"] = "[!include[](includes/" + unit.get('unit') + ")]"

        with open(filename, 'w', encoding='utf8') as file:
            file.write("### YamlMime:ModuleUnit\n")
            yaml.dump(output, file, default_flow_style = False, allow_unicode = True, encoding = None, width=1000)


def main():
    """Generate units from yaml file."""

    delete_output_folder()

    # Read the yaml file
    with open(os.path.join(INPUT_FOLDER, MODULE_FILE), encoding='utf8') as quiz:
        root = yaml.load(quiz, Loader=yaml.Loader)
    
        create_module_yml(root)
        create_index_yml(root)
        copy_source_files()
        print("Done")


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_folder")
    parser.add_argument("-o", "--output_folder")

    args = parser.parse_args()

    INPUT_FOLDER = args.input_folder
    OUTPUT_FOLDER = args.output_folder

    main()
