import json
from pathlib import Path
from notion.client import NotionClient
from notion.block import TodoBlock, PageBlock, TextBlock, VideoBlock
import random as r

from loguru import logger

from py_files.some_functions import set_logger
from requests import HTTPError


def unpack_words_file(path):
    with open(path, 'r', encoding='UTF-8') as words_file:
        words_list = words_file.read()
        words_list = words_list.split('\n')
        return words_list


def fill_to_do(stop_count, link):
    x = 0
    page = client.get_block(link)
    while x < stop_count:
        x += 1
        new_page = page.children.add_new(PageBlock, title=words_list[r.randint(1, 1500000)])
        new_page_link = new_page.get_browseable_url()
        page_to_fill = client.get_block(new_page_link)

        count_of_strings = 0

        stop_count_of_strings = r.randint(10, 20)
        while count_of_strings < stop_count_of_strings:
            count_of_strings += 1
            one_string = ''

            count_of_words = 0

            stop_count_of_words = r.randint(3, 10)
            while count_of_words < stop_count_of_words:
                count_of_words += 1
                one_string += words_list[r.randint(1, 1500000)] + ' '
                # if one_string == '':
                #     logger.debug('Пустая строка')

            # logger.debug(f'Строка: {one_string}')
            try:
                page_to_fill.children.add_new(TodoBlock, title=one_string)

            except HTTPError:
                logger.critical('Соединение нарушено. HTTPError')

        logger.info(f'Создано to-do-списков: {x}/{stop_count}')


def fill_abstract(stop_count, link):
    x = 0
    page = client.get_block(link)

    while x < stop_count:
        x += 1
        new_page = page.children.add_new(PageBlock, title=words_list[r.randint(1, 1500000)])
        new_page_link = new_page.get_browseable_url()
        page_to_fill = client.get_block(new_page_link)

        count_of_words = 0
        text_string = ''

        text_video_repeat = 0
        stop_count_text_video_repeat = r.randint(1, 5)

        while text_video_repeat < stop_count_text_video_repeat:
            stop_count_of_words = r.randint(100, 1000)

            while count_of_words < stop_count_of_words:
                count_of_words += 1
                text_string += words_list[r.randint(1, 1500000)] + ' '
                # if one_string == '':
                #     logger.debug('Пустая строка')

            text_video_repeat += 1

            page_to_fill.children.add_new(TextBlock, title=text_string)

            video = page_to_fill.children.add_new(VideoBlock, width=800)
            video.set_source_url('https://www.youtube.com/watch?v=oHg5SJYRHA0')

            text_string = ''

        logger.info(f'Создано конспектов: {x}/{stop_count}')


logger.info('Скрипт завершил работу')

set_logger()


with open(Path('Google Keep', '03.10.17.json'), 'r', encoding='UTF-8') as note_file:
    note_dict = json.load(note_file)
    print(note_dict['listContent'][0]['text'])

client = NotionClient(
    token_v2="e9301426f5180b643e1189d5ca2321f6f743effbebe9eea54321f48aa8740a37e8d578e391f0d370f398c2f8e4b3722a6a15e933b24b280769ab81a33be1ba696856981fc422751800353343d983")

words_list = unpack_words_file(Path('russian-words', 'russian.txt'))

fill_to_do(642, 'https://www.notion.so/To-do-90aabdeedada4726bc82ae815c257346')

fill_abstract(500, 'https://www.notion.so/bc5092f4958047809758392bcf103d1d')
