#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import logging
import json


def start_logging():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    stream = logging.StreamHandler()
    logger.addHandler(stream)

    return logger


def start():
    args = sys.argv
    if len(args) < 2:
        return Exception("Not target specified")

    target_dir = args[1]
    logger.info('Starting to analyze "%s"', target_dir)
    abs_path = get_absolute_path(target_dir)
    ls = get_files_in_target_folder(abs_path)
    create_file_json_in_script_folder(ls, target_dir)


def get_absolute_path(path):
    absolute_path = os.path.abspath(path)
    return absolute_path


def get_files_in_target_folder(target_dir):
    files = os.listdir(target_dir)

    if 'JSON.txt' in os.listdir('.'):
        with open('JSON.txt', 'r') as out:
            old_data = json.load(out)

            if old_data['target'] != target_dir:
                return files

            changes = list(set(files) ^ set(old_data.values()))
            changes.remove(target_dir)
            if len(changes) >= 1:
                logger.info("Changes: %s", changes)
            else:
                logger.info("Changes not found.")
    return files


def create_file_json_in_script_folder(files, target_dir):
    files_dict = {"имя_файла" + str(n): files[n] for n in range(len(files))}
    files_dict['target'] = get_absolute_path(target_dir)
    files_json = json.dumps(files_dict, sort_keys=True,
                            indent=4, ensure_ascii=False)
    with open('JSON.txt', 'w') as infile:
        infile.write(files_json)


logger = start_logging()
BASE_DIR = os.path.dirname(os.path.abspath(__name__))
start()
