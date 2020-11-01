import json
import os
import shutil
from pathlib import Path
from notion.client import NotionClient
from notion.block import TodoBlock, PageBlock, TextBlock, VideoBlock
import random as r
from os import listdir, mkdir

from loguru import logger

from py_files.some_functions import set_logger
from requests import HTTPError


set_logger()

notes_list = listdir('Google Keep')

def files_sorting(folder_all_notes_name, hashtag):
    if os.path.exists(Path(folder_all_notes_name, hashtag)):
        shutil.rmtree(Path(folder_all_notes_name, hashtag))
    os.mkdir(Path(folder_all_notes_name, hashtag))

    notes_count = 0
    for file_name in notes_list:
        notes_count += 1
        logger.debug(f'Обработано заметок: {notes_count}/{len(notes_list)}')
        if '.json' in file_name:
            with open(Path(folder_all_notes_name, file_name), 'r', encoding='UTF-8') as note_file:
                note_dict = json.load(note_file)

                try:
                    hashtag_value = note_dict['labels'][0]['name']

                except:
                    continue

                if hashtag_value == 'Инфа':
                    shutil.copy(Path(folder_all_notes_name, file_name), Path(folder_all_notes_name, hashtag))



files_sorting('Google Keep', 'Инфа')

# with open(Path('Google Keep', '03.10.17.json'), 'r', encoding='UTF-8') as note_file:
#     note_dict = json.load(note_file)
#     print(note_dict['listContent'][0]['text'])

