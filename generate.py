"""
Python app to read a blog.yaml and generate a blog file structure
and index.md markdown file from a template
"""

import os
import pathlib
import argparse
import jinja2   # https://pypi.org/project/Jinja2/
import oyaml as yaml
import shutil


TEMPLATE_FILE = "module.md"
INDEX_TEMPLATE = "index.template"
INDEX_YAML = "index.yml"
MODULE_FILE = "module.yml"

MEDIA_FOLDER = "media"
INCLUDES_FOLDER = "includes"
SOURCE_FOLDER = "source"
RESOURCES_FOLDER = "resources"

input_folder = None
output_folder = None


def set_key_value(units, unit, key):
    unit[key] = unit.get(key, units['module'][key])


def delete_output_folder():
    """Reset the output folder"""

    if os.path.exists(output_folder):
        shutil.rmtree(os.path.join(output_folder))

    pathlib.Path(output_folder).mkdir(parents=True, exist_ok=True)


def copy_source_files():

    pathlib.Path(os.path.join(output_folder, INCLUDES_FOLDER)
                 ).mkdir(parents=True, exist_ok=True)
    for filename in os.listdir(os.path.join(input_folder, SOURCE_FOLDER)):
        if filename.endswith(".md"):
            src = os.path.join(input_folder, SOURCE_FOLDER, filename)
            dst = os.path.join(output_folder, INCLUDES_FOLDER, filename)
            shutil.copy2(src, dst)

    src = os.path.join(input_folder, MEDIA_FOLDER)
    dst = os.path.join(output_folder, MEDIA_FOLDER)
    shutil.copytree(src, dst)

    src = os.path.join(input_folder, RESOURCES_FOLDER)
    dst = os.path.join(output_folder, RESOURCES_FOLDER)
    shutil.copytree(src, dst)


def get_module_key_value(units, key):
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
            unit["unit"].lower().replace(' ', '-')
        index["units"].append(uid)

    filename = os.path.join(output_folder, INDEX_YAML)
    with open(filename, 'w', encoding='utf8') as file:
        file.write("### YamlMime:Module\n")
        yaml.dump(index, file)


def main():
    """Generate units from yaml file."""

    delete_output_folder()

    # Read the yaml file
    with open(os.path.join(input_folder, MODULE_FILE), encoding='utf8') as quiz:
        root = yaml.load(quiz, Loader=yaml.Loader)

    # Read the template file
    template_loader = jinja2.FileSystemLoader(searchpath="./")
    template_env = jinja2.Environment(loader=template_loader)

    template = template_env.get_template(TEMPLATE_FILE)

    for unit in root['module']['units']:

        set_key_value(root, unit, 'uid_root')
        set_key_value(root, unit, 'date')
        set_key_value(root, unit, 'author')
        set_key_value(root, unit, 'topic')
        set_key_value(root, unit, 'prod')
        set_key_value(root, unit, 'custom')

        markdown_filename = unit.get('unit') + ".md"
        markdown_filename = os.path.join(
            input_folder, SOURCE_FOLDER, markdown_filename)

        quiz_filename = unit.get('unit') + ".yml"
        quiz_filename = os.path.join(
            input_folder, SOURCE_FOLDER, quiz_filename)

        if os.path.isfile(markdown_filename):
            pass
        elif os.path.isfile(quiz_filename):
            with open(quiz_filename, encoding='utf8') as quiz:
                unit['quiz'] = quiz.read()
        else:
            print("Unit file .md or .yml not found for: " + unit['unit'])
            exit()

        output_text = template.render(unit)

        unit = unit.get('unit') + ".yml"

        filename = os.path.join(output_folder, unit)

        with open(filename, 'w', encoding='utf8') as quiz:
            quiz.write(output_text)

    create_index_yml(root)
    copy_source_files()
    print("Done")


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_folder")
    parser.add_argument("-o", "--output_folder")

    args = parser.parse_args()

    input_folder = args.input_folder
    output_folder = args.output_folder

    main()
