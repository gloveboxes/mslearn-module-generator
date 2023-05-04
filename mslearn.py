"""
Python app to generate a MS Learn compliant module from a markdown files and a yaml module definition file
"""

import os
import pathlib
import argparse
import math
import oyaml as yaml
import shutil


INDEX_YAML = "index.yml"
MODULE_DEFINITION = "module.yml"

INCLUDES_FOLDER = "includes"
MEDIA_FOLDER = "media"
RESOURCES_FOLDER = "resources"
SOURCE_FOLDER = "source"

INPUT_FOLDER = None
OUTPUT_FOLDER = None

AVG_READING_WORDS_PER_MINUTE = 250

UNIT_TEMPLATE = """
[//]: # (1. Topic sentences)\n\n
[//]: # (   Goal: briefly summarize the key skills this unit will teach)\n\n
"""


QUIZ = """
questions:
  - content: "Sample question with multichoice answers?"
    choices:
      - content: "Answer option 1"
        isCorrect: false
        explanation: "Answer option 1 is incorrect because..."
      - content: "Sample answer option 2"
        isCorrect: true
        explanation: "Answer option 2 is correct because..."
      - content: "Answer option 3"
        isCorrect: false
        explanation: "Answer option 3 is incorrect because..."
  - content: "Sample question with multichoice answers?"
    choices:
      - content: "Answer option 1"
        isCorrect: false
        explanation: "Answer option 1 is incorrect because..."
      - content: "Sample answer option 2"
        isCorrect: true
        explanation: "Answer option 2 is correct because..."
      - content: "Answer option 3"
        isCorrect: false
        explanation: "Answer option 3 is incorrect because..."
"""


def delete_output_folder():
    """Reset the output folder"""

    if os.path.exists(OUTPUT_FOLDER):

        print("")
        print("You are about to delete the Learn Output Folder {OUTPUT_FOLDER}.")
        print("Are you sure you wish to delete? (y/n)", end="")

        answer = input().lower().strip()
        if answer == "y":
            shutil.rmtree(os.path.join(OUTPUT_FOLDER))
        else:
            print("Exiting...")
            exit()

    pathlib.Path(OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)


def copy_source_files():
    """Copy project assets to MS Learning format"""

    # Copy all the markdown files to the includes folder
    pathlib.Path(os.path.join(OUTPUT_FOLDER, INCLUDES_FOLDER)).mkdir(parents=True, exist_ok=True)

    for filename in os.listdir(os.path.join(INPUT_FOLDER, SOURCE_FOLDER)):
        if filename.endswith(".md"):
            src = os.path.join(INPUT_FOLDER, SOURCE_FOLDER, filename)
            dst = os.path.join(OUTPUT_FOLDER, INCLUDES_FOLDER, filename)
            shutil.copy2(src, dst)

    # Copy all the media files to the media folder
    src = os.path.join(INPUT_FOLDER, MEDIA_FOLDER)
    dst = os.path.join(OUTPUT_FOLDER, MEDIA_FOLDER)
    shutil.copytree(src, dst)

    # Copy all the resources files to the resources folder
    src = os.path.join(INPUT_FOLDER, RESOURCES_FOLDER)
    dst = os.path.join(OUTPUT_FOLDER, RESOURCES_FOLDER)
    shutil.copytree(src, dst)


def get_key_value(root, key):
    """get key from module"""
    return root.get(key)


def get_unit_key_value(root, unit, key):
    """get key from unit if not found then get from module"""
    return unit.get(key, root.get(key))


def create_uid(root, unit):
    """Create the uid for the unit"""
    return root.get('uid_root') + "." + unit["unit"].lower().replace(' ', '-').split(".")[0]


def calculate_read_time(text):
    """Calculate the read time for a unit"""
    word_count = len(text.split())
    reading_time = math.ceil(word_count / AVG_READING_WORDS_PER_MINUTE)
    return reading_time


def create_module_index_yml(root):
    """Create the index.yml file"""

    index = {
        "uid": root.get('uid_root'),
        "metadata":
            {"title": get_key_value(root, 'title'),
                "description": get_key_value(root, 'description'),
                "author": get_key_value(root, 'author'),
                "ms.date": get_key_value(root, 'date'),
                "ms.author": get_key_value(root, 'ms.author'),
                "ms.topic": get_key_value(root, 'topic'),
                "ms.prod": get_key_value(root, 'prod'),
                "ms.custom": get_key_value(root, 'custom')
             },
        "title": get_key_value(root, 'title'),
        "summary": get_key_value(root, 'summary'),
        "abstract": get_key_value(root, 'abstract'),
        "prerequisites": get_key_value(root, 'prerequisites'),
        "levels": get_key_value(root, 'levels'),
        "roles": get_key_value(root, 'roles'),
        "products": get_key_value(root, 'products'),
        "subjects": get_key_value(root, 'subjects'),
        "badge": {"uid": get_key_value(root, 'uid_root') + ".badge"},
        "units": []
    }

    for unit in root['units']:
        index["units"].append(create_uid(root, unit))

    filename = os.path.join(OUTPUT_FOLDER, INDEX_YAML)
    with open(filename, 'w', encoding='utf8') as file:
        file.write("### YamlMime:Module\n")
        yaml.dump(index, file)


def create_new_content_file(unit, unit_filename):
    """Create the new content file"""
    with open(unit_filename, encoding='utf8', mode='w') as file:
        if unit_filename.endswith(".md"):
            title = unit.get('title')
            description = unit.get('description')
            file.write(f'[//]: # ({title})\n')
            file.write(f'[//]: # ({description})\n')
            file.write(UNIT_TEMPLATE)
        if unit_filename.endswith(".yml"):
            title = unit.get('title')
            description = unit.get('description')
            file.write(f'# {title}\n')
            file.write(f'# {description}\n')
            file.write('# The following is an example with two multichoice questions\n')
            yaml.dump(yaml.safe_load(QUIZ), file, width=1000)


def create_module_unit_yml(root):
    """Create the module.yml file"""
    for unit in root['units']:

        unit_filename = unit.get('unit')
        unit_filename = os.path.join(
            INPUT_FOLDER, SOURCE_FOLDER, unit_filename)

        if os.path.isfile(unit_filename):
            text = open(unit_filename, encoding='utf8').read()

            if unit_filename.endswith(".yml"):
                question = yaml.load(text, Loader=yaml.Loader)
                unit['quiz'] = question

            if unit.get('durationInMinutes') is None:
                unit['durationInMinutes'] = calculate_read_time(text)
        else:
            create_new_content_file(unit, unit_filename)

        output = {
            "uid": create_uid(root, unit),
            "title": unit.get('title'),
            "metadata": {
                "title": unit.get('title'),
                "description": unit.get('description'),
                "ms.date": get_unit_key_value(root, unit, 'date'),
                "author": get_unit_key_value(root, unit, 'author'),
                "ms.author": get_unit_key_value(root, unit, 'ms.author'),
                "ms.topic": get_unit_key_value(root, unit, 'topic'),
                "ms.prod": get_unit_key_value(root, unit, 'prod'),
                "ms.custom": get_unit_key_value(root, unit, 'custom')
            },
            "durationInMinutes": unit.get('durationInMinutes')
        }

        if unit.get('quiz') is not None:
            output["quiz"] = unit.get('quiz')
        else:
            output["content"] = "[!include[](includes/" + \
                unit.get('unit') + ")]"

        unit_file = unit.get('unit').split(".")[0] + ".yml"
        filename = os.path.join(OUTPUT_FOLDER, unit_file)

        with open(filename, 'w', encoding='utf8') as file:
            file.write("### YamlMime:ModuleUnit\n")
            yaml.dump(output, file, width=100)


def main():
    """Generate units from yaml file."""

    if os.path.isdir(INPUT_FOLDER):

        delete_output_folder()

        filename = os.path.join(INPUT_FOLDER, MODULE_DEFINITION)
        if os.path.isfile(filename):
            # Read the yaml file
            with open(filename, encoding='utf8') as quiz:
                root = yaml.load(quiz, Loader=yaml.Loader)

                create_module_unit_yml(root)
                create_module_index_yml(root)
                copy_source_files()
                print("Done")
        else:
            print("Module definition file not found: " + filename)
    else:
        print("Input folder not found: " + INPUT_FOLDER)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--project")
    parser.add_argument("-m", "--module")

    args = parser.parse_args()

    INPUT_FOLDER = args.project
    OUTPUT_FOLDER = args.module

    main()
