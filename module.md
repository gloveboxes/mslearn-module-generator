{% set uid = uid_root ~ '.' ~ unit | lower | replace(" ", "-") -%}
### YamlMime:ModuleUnit
uid: {{ uid }}
title: {{ title }}
metadata:
  title: {{ title }}
  description: {{ description }}
  ms.date: {{ date }}
  author: {{ author }}
  ms.author: {{ author }}
  ms.topic: {{ topic }}
  ms.prod: {{ prod }}
  ms.custom: {{ custom }}
durationInMinutes: {{ durationInMinutes }}
{% if quiz -%}
content: |
  quiz:
    {{ quiz }}
{% else -%}
content: |
  [!include[](includes/{{ unit }}.md)]
{%- endif %}

