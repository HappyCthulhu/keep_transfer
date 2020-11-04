import json
import os
import shutil
from pathlib import Path
from notion.client import NotionClient
from notion.block import TodoBlock, PageBlock, TextBlock, VideoBlock, ImageBlock
import random as r
from os import listdir, mkdir

from loguru import logger

from py_files.some_functions import set_logger
from requests import HTTPError

# TODO: Добавить проверку на архивацию
# TODO: Добавить проверку на закрепленность
# TODO: Добавить проверку наличия картинок


set_logger()


def pictures_collect(attachments):
    for picture in attachments:
        picture_name = picture['filePath']
        shutil.copy(Path(MAIN_FOLDER, picture_name), Path(MAIN_FOLDER, HASHTAG, picture_name))


def check_hashtag_folder_exist(hashtag_name):
    if os.path.exists(Path('Google Keep', hashtag_name)):
        return True
    else:
        return False


def check_is_pinned(dict_with_notes_value, list_with_all_notes_value):
    if dict_with_notes_value['isPinned']:
        list_with_all_notes_value.insert(0, dict_with_notes_value)
    else:
        list_with_all_notes_value.append(dict_with_notes_value)
    return list_with_all_notes_value


def hashtag_folder_sort(hashtag_name):
    notes_list = listdir(Path('Google Keep', hashtag_name))
    notes_value_list = []
    notes_count = 0
    for file_name in notes_list:
        notes_count += 1
        logger.debug(f'Обработано заметок: {notes_count}/{len(notes_list)}')

        if '.json' in file_name:
            with open(Path('Google Keep', hashtag_name, file_name), 'r', encoding='UTF-8') as note_file:
                logger.debug(note_file)
                note_dict = json.load(note_file)
            notes_value_list = check_is_pinned(note_dict, notes_value_list)

            if 'attachments' in note_dict:
                try:
                    pictures_collect(note_dict['attachments'])
                except FileNotFoundError:
                    logger.critical('В папке нет указанных прикрепленных материалов')


    return notes_value_list


def files_sorting(folder_all_notes_name, hashtag):
    notes_list = listdir(Path('Google Keep'))
    os.mkdir(Path(folder_all_notes_name, hashtag))

    notes_value_list = []
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

                if hashtag_value == hashtag:
                    shutil.copy(Path(folder_all_notes_name, file_name), Path(folder_all_notes_name, hashtag))

                    notes_value_list = check_is_pinned(note_dict, notes_value_list)

                if 'attachments' in note_dict:
                    try:
                        pictures_collect(note_dict['attachments'])
                    except FileNotFoundError:
                        logger.critical('В папке нет указанных прикрепленных материалов')

    return notes_value_list


def notion_upload(list_of_notes, collection_link):
    page = client.get_block(collection_link)

    count_of_notes = 0

    for note in list_of_notes:
        count_of_notes += 1

        # try:
        note_title = note['title']
        # except AttributeError:
        #     note_title = 'Без названия'

        new_page = page.children.add_new(PageBlock, title=note_title)
        new_page_link = new_page.get_browseable_url()
        page_to_fill = client.get_block(new_page_link)

        logger.debug(note)

        if 'attachments' in note:
            for picture in note['attachments']:
                picture_name = picture['filePath']
                picture_load = open(Path(MAIN_FOLDER, HASHTAG, picture_name))
                image = page_to_fill.children.add_new(ImageBlock, width=800)
                image.upload_file(picture_load)

            if 'listContent' in note:
                logger.debug('To-do')
                for text in note['listContent']:
                    to_do_element = page_to_fill.children.add_new(TodoBlock, title=text['text'])
                    if text['isChecked']:
                        to_do_element.checked = True
                    else:
                        to_do_element.checked = False

            elif 'textContent' in note:
                logger.debug('Обычный текст')
                pass
                page_to_fill.children.add_new(TextBlock, title=note['textContent'])
            else:
                logger.critical('Формат записки не определен')

            if note['isArchived']:
                page_to_fill.remove()

            logger.info(f'Создано заметок: {count_of_notes}/{len(list_of_notes)}')

        else:
            continue



HASHTAG = 'Дела'
MAIN_FOLDER = 'Google Keep'

if check_hashtag_folder_exist(HASHTAG):
    notes_list_value = hashtag_folder_sort(HASHTAG)
else:
    notes_list_value = files_sorting(MAIN_FOLDER, HASHTAG)

client = NotionClient(
    token_v2="e9301426f5180b643e1189d5ca2321f6f743effbebe9eea54321f48aa8740a37"
             "e8d578e391f0d370f398c2f8e4b3722a6a15e933b24b280769ab81a33be1ba696856981fc422751800353343d983")

notion_upload(notes_list_value, 'https://www.notion.so/Test-dee31db8ac314350a8e193134675eb44')
# with open(Path('Google Keep', '03.10.17.json'), 'r', encoding='UTF-8') as note_file:
#     note_dict = json.load(note_file)
#     print(note_dict['listContent'][0]['text'])
