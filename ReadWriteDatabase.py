#!/usr/bin/python
# -*- coding: utf8 -*-
import json


def read_json(json_file_path: str) -> tuple:
    with open(json_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data, len(data)


def write_json(json_file_path: str, name_text: str, new_text: str) -> None:
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    data[name_text] = new_text
    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def read_txt_and_write_to_json(txt_file_path: str, json_file_path: str, name_text: str) -> None:
    try:
        with open(txt_file_path, 'r', encoding='utf-8') as txt_file:
            text_content = txt_file.read()
        write_json(json_file_path, name_text, text_content)
    except Exception as e:
        print(f'Error: {e}')
