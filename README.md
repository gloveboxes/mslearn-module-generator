# MS Learn Module Generator

The MS Learn Module Generator simplifies creating and maintaining MS Learn modules. You focus on the content, and the generator looks after the scaffolding and metadata.

## Background

If you've worked on MS Learn modules, you'll appreciate there are two aspects to creating a learn Module. There is the content for the learner and the scaffolding. The scaffolding is the metadata and the structure of the Module. As you create the content you need to keep the scaffolding in sync.

Keeping scaffolding and metadata in sync can be fiddly, error-prone, and time-consuming, especially as content development evolves. You'll find you are constantly updating the scaffolding and metadata in multiple places.

This project aims to simplify creating and maintaining MS Learn modules. You focus on the content, and the generator creates the scaffolding and metadata. You define **one** Module definition file that describes both the Module and Module Units, and the generator creates the Module structure and metadata from this definition.

## Getting Started

Clone this repository to your local machine.

```bash
git clone https://github.com/gloveboxes/mslearn-module-generator.git
```

### Understanding the MS Learn Content Structure

The root of the repo contains the following files and folders:

- `mslearn.py` - the main script that generates the MS Learn Module content.
- `requirements.txt` - the Python libraries required to run the script.
- `sample-project` - a sample project that contains the content for a learn Module.

In the sample project folder, you'll find the following files and folders:

- `module.yml` - the Module definition file.
- `module.json` - the schema file for the Module definition file.
- `source` - the folder that contains the content for the Module. Add your markdown (.md) and knowledge check (.yml) files to this folder.
- `media` - the folder that contains the images for the Module. Add the images for the Units to this folder.
- `resources` - the folder that contains the resources for the Module. Add your resources to this folder. For example, you might have a PowerPoint file you've used to create the images for the Module. The resources folder is a great place to store these files.

### Understanding the Module Definition File

The Module definition file is a yaml file that describes the Module and Units. The Module definition file is used by the generator to create the Module structure and metadata.

The learn Module definition file describes the following:

- The Learn Module metadata. For example, the Learn Module date, author, description, etc.
- The Units that make up the Module including their metadata. The title, description, and the name of the markdown or knowledge check file.

Here is an example of a Module definition file:

```yaml
uid_root: learn.microsoft.develop-intelligent-app-azure-openai
title: "Develop an intelligent app with Azure OpenAI Services"
iconUrl: /training/achievements/student-evangelism/develop-secure-iot-solutions-with-azure-sphere.svg
date: 05/04/2023
author: gloveboxes
topic: interactive-tutorial
prod: learning-azure-openai
custom: team=nextgen
subjects: [ai, cloud-computing]
products: [azure-openai-services]
roles: [ai-developer]
levels: [intermediate]

summary: Create a static web app using Azure Static Web Apps and learn about Azure OpenAI Services

abstract: |
  In this Module, you will:
  - Create a static web app using Azure Static Web Apps
  - Create an Azure OpenAI Service

prerequisites: |
  - prerequisite: 1
  - prerequisite: 2

units:
  - unit: 1-Introduction.md
    title: Introduction
    description: In this section, we help the learner to decide if the product meets their needs. We'll explain when to use the product and how it works.

  - unit: 2-design-intelligent-solution.md
      title: Design a secure IoT solution with Azure Sphere
      description: In this section, we help the learner to design an intelligent app with the Azure OpenAI Service.

  - unit: 3-build-intelligent-solution.md
      ...
      ...
```

Notes:
- The order of the Units in the Module definition file is the order they will appear in the Learn Module. It's easy to reorder or rename Units. When you've finished your updates, rerun the generator to update the Learn Module metadata.
- The Unit durationInMinutes is automatically calculated from the Unit markdown file. The calculation is based on an average reading speed of 250 words per minute. You can override the calculated value by adding a durationInMinutes value to the Unit definition. See the [Overriding default metadata](#overriding-default-metadata) for more information.

### Prerequisites

Install the following:

- Python 3.10 or higher and pip
- Pip install the required libraries: `pip install -r requirements.txt`

## Workflow

The workflow for creating a Module is as follows:

1. Define your Module in the Module definition file.
1. Run the generator script. The generator will:
   1. Create empty Unit markdown and knowledge check files in the project `source` folder (if they don't already exist).
   1. Create the MS Learn Module.
1. Write the content for each Unit.
1. Rerun the generator script to update the Module with your newly written content.
1. When happy with the content, submit a PR to the MS Learn `learn-pr` repo.
2. You'll almost certainly need to make changes to the Module as it goes through the review process. Make your changes, rerun the generator script to update the Module, and resubmit the PR.

## Define your Module

1. Use the existing `sample-project` as a template for your Module. Copy/rename the `sample-project` folder to match the name of your Learn Module.
1. Given you cloned the repo to your local machine, you'll want to make the repo your own. Navigate to the repo you just cloned, delete the .git folder, and then `git init` the folder.
1. Open the Module definition file `module.yml` in VS Code.
1. Install the [YAML extension](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml).
2. Update the Module metadata.
3. Create the Unit definitions.
4. Save the Module definition file.

## Run the MS Learn Generator script

1. Open a terminal window and navigate to the root of the repo.
1. Run the generator script: `python mslearn.py --project <path to your module folder> --output <path to the output folder>`

    For example, if your Module project folder is called `my-module` and it's located in the root of the repo you cloned, then you would run the following command:

    ```bash
    python mslearn.py -p my-learn-project -m ../my-learn-module
    ```

    The `-m` parameter should point to the appropriate folder location in the MS Learn `learn-pr` repo you separately cloned to your computer.

    The generator will create the MS Learn Module. The following happens when you run the generator script:
    - All the MS Learn Module metadata .yml files for the Module and Units are generated.
    - The markdown files in the project `source` folder are copied to the MS Learn `includes` folder.
    - The images from the project `media` folder are copied to the MS Learn `media` folder.
    - The resources from the project `resources` folder are copied to the MS Learn `resources` folder.


## Overriding default metadata

The generator aims to minimize the metadata you need to define for each unit, but there will be times when you need to override the defaults. You can add the following metadata in a Unit definition to override the defaults:

  - author
  - date
  - topic
  - prod
  - custom
  - durationInMinutes

    For example, if you want to override the author, the date, and the durationInMinutes for a Unit you would add the following to the Unit definition:

    ```yaml
      - unit: 1-Introduction.md
        title: Introduction
        description: In this section, we help the learner to decide if the product meets their needs. We'll explain when to use the product and how it works.

        author: leestott
        date: 05/05/2023
        durationInMinutes: 10
    ```

## Knowledge check files

The knowledge check file is a yaml file that contains the questions and answers for a knowledge check Unit. Knowledge check files must have an extension of .yml. The following is an example of a knowledge check file:

```yaml
questions:
  - content: "In the Azure Sphere ecosystem, which component is missing from the following list: Azure Sphere SDK, Azure Sphere tenant, Azure Sphere OS?"
    choices:
      - content: "Azure Sphere API"
        isCorrect: false
        explanation: "Azure Sphere API isn't a component of the Azure Sphere ecosystem."
      - content: "Azure Sphere Security Service"
        isCorrect: true
        explanation: "Azure Sphere Security Service is a key component of the Azure Sphere ecosystem."
      - content: "Azure Sphere Security Key"
        isCorrect: false
        explanation: "Azure Sphere Security Key isn't a component of the Azure Sphere ecosystem."
  - content: "Your organization created an Azure Sphere tenant and then claimed each of its devices into that tenant. What function does this accomplish?"
    choices:
      - content: "You can manage those devices remotely and securely."
        isCorrect: true
        explanation: "The tenant allows you to manage devices remotely and securely."
      - content: "The tenant allows devices to communicate better with other tenants."
        isCorrect: false
        explanation: "The tenant doesn't enable communication between other tenants."
      - content: "Your organization can name individual devices."
        isCorrect: false
        explanation: "The tenant doesn't enable naming of devices."
```
